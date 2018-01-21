from datetime import datetime
import multiprocessing
import os
import signal
import time

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from TwitterAPI import TwitterAPI, TwitterConnectionError

from base.fields import UnsignedBigIntegerField
from crowdgezwitscher.log import logger
from events.models import Event
from twitter import utils


class TwitterAccount(models.Model):
    name = models.CharField(max_length=15, unique=True)
    account_id = UnsignedBigIntegerField(unique=True)
    last_known_tweet_id = UnsignedBigIntegerField(default=0)
    events = models.ManyToManyField(Event, blank=True, related_name="twitter_accounts")

    def __repr__(self):
        return '<TwitterAccount %s>' % self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('twitter:detail', kwargs={'pk': self.pk})

    def clean(self):
        # remove leading @
        if self.name.startswith('@'):
            self.name = self.name[1:]

        twitter = TwitterAPI(settings.TWITTER_CONSUMER_KEY,
                             settings.TWITTER_CONSUMER_SECRET,
                             auth_type='oAuth2')
        try:
            user = twitter.request('users/show', {'screen_name': self.name}).json()
        except TwitterConnectionError:
            logger.warning("Could not connect to Twitter.")
            raise ValidationError("Could not connect to Twitter to retrieve user_id.")
        if 'id' in user:
            self.account_id = user['id']
        else:
            logger.warning("Could not find user with provided name.")
            raise ValidationError("Could not find user with provided name.")

        if TwitterAccount.objects.filter(account_id=self.account_id):
            logger.warning("TwitterAccount with account_id is already in database.")
            raise ValidationError("Twitter account with this name already exists.")

    def _fetch_tweets_from_api(self, twitter, max_id=None, since_id=None, count=200, trim_user=True):
        request_parameters = {
            'count': count,
            'user_id': self.account_id,
            'trim_user': trim_user,
            'exclude_replies': False,
            'contributor_details': False,
        }

        # max_id is optional and not known for first request
        if max_id:
            request_parameters['max_id'] = max_id
        # since_id is optional and used to get newer tweets than those already saved
        if since_id:
            request_parameters['since_id'] = since_id

        return twitter.request('statuses/user_timeline', request_parameters).json()

    def _get_utc_offset(self, twitter):
        tweets = self._fetch_tweets_from_api(twitter, None, None, 1, False)
        if len(tweets) > 0:
            return tweets[0]['user']['utc_offset'] or 0

    def fetch_tweets(self, timeout=300):
        """Runs _fetch_tweets with the given timeout in seconds."""
        p = multiprocessing.Process(target=self._fetch_tweets)
        p.start()
        p.join(timeout)
        if p.is_alive():
            logger.warning("Timeout for _fetch_tweets. Terminating.")
            p.terminate()  # SIGTERM
            time.sleep(0.5)  # give the termination some time
            if p.is_alive():
                logger.warning("_fetch_tweets refuses to terminate. Will kill it.")
                os.kill(p.pid, signal.SIGKILL)  # nuke it. RIP.
            p.join()


    def _fetch_tweets(self):
        # Fetching tweets can require multiple request to Twitter's API.
        # This algorithm first fetches the newest tweets and fetches increasingly older ones with every subsequent
        # request.
        # The algorithm is based on Twitter's suggestions on "Working with Timelines":
        # https://dev.twitter.com/rest/public/timelines
        # General information about the used API can be found here:
        # https://dev.twitter.com/rest/reference/get/statuses/user_timeline

        if not utils.lock_twitter():
            return

        new_tweets = []
        tweet_hashtag_mappings = {}
        twitter = TwitterAPI(settings.TWITTER_CONSUMER_KEY,
                             settings.TWITTER_CONSUMER_SECRET,
                             auth_type='oAuth2')

        last_known_tweet_id = None
        should_brake = False
        try:
            # Twitter does somehow not reflect the combination of timezone and daylight savings time correctly
            utc_offset = self._get_utc_offset(twitter)
            # Fetch 1st batch of tweets but only ones we do not already have in the database. Therefore, we set
            # since_id to the newest tweet's ID we already have. This will return the newest tweets for the account.
            # If there are more new tweets than we can get in a single request, we will get the older ones later.
            tweets_from_api = self._fetch_tweets_from_api(twitter, since_id=self.last_known_tweet_id)
            if tweets_from_api:
                # Extract the newest tweet's ID for the account. However, we will not store this reference in the DB
                # until all new tweets have been fetched and saved.
                last_known_tweet_id = tweets_from_api[0]['id']
            while tweets_from_api:
                for tweet_from_api in tweets_from_api:
                    # Check if received tweet is already in DB.
                    # If so, break, as we already have all following tweets (Twitter sends newest tweets first)
                    if tweet_from_api['id'] <= self.last_known_tweet_id:
                        should_brake = True  # a hint to also break out of the outer loop
                        break
                    # Parses twitter date format, converts to timestamp, adds utc_offset and creates datetime object
                    try:
                        created_at = timezone.make_aware(
                            datetime.fromtimestamp(
                                time.mktime(
                                    time.strptime(
                                        tweet_from_api['created_at'],
                                        '%a %b %d %H:%M:%S +0000 %Y')
                                ) + utc_offset
                            )
                        )
                    except ValueError:
                        logger.warning("Got unexpected result while fetching tweets and parsing their creation times.")
                        continue
                    is_reply = tweet_from_api['in_reply_to_user_id'] is not None
                    tweet = Tweet(tweet_id=tweet_from_api['id'],
                                  content=tweet_from_api['text'],
                                  created_at=created_at,
                                  is_reply=is_reply,
                                  account=self)
                    new_tweets.append(tweet)
                    hashtags = []
                    for hashtag_from_api in tweet_from_api['entities']['hashtags']:
                        hashtag_text = hashtag_from_api['text'].lower()
                        hashtag, _ = Hashtag.objects.get_or_create(hashtag_text=hashtag_text)
                        hashtags.append(hashtag)
                    tweet_hashtag_mappings[tweet.tweet_id] = hashtags
                if should_brake:
                    break
                # Fetch next batch of older tweets. Therefore, set max_id to the oldest tweet's ID that we already
                # processed. As max_id is inclusive and we do not want to receive the same tweet again, we substract 1
                # from the oldest tweet's ID.
                tweets_from_api = self._fetch_tweets_from_api(
                    twitter,
                    max_id=tweets_from_api[-1]['id'] - 1)
        except Exception as e:  # broad exception clause as we need to unlock in any case.
            exception_log_map = {
                TwitterConnectionError: "Could not connect to Twitter.",
                KeyError: "Got unexpected result while fetching tweets."
            }
            logger.warning(exception_log_map.get(
                type(e),
                "Got unexpected exception while fetching tweets: %s - %s" % (type(e), e)
            ))

            utils.unlock_twitter()

            # We return here without saving any possibly already fetched tweets.
            # If we would save them, we would also save last_known_tweet_id. So on the next run of this function, we
            # would not fetch any tweets older than last_known_tweet_id. So if the error occurred before all tweets were
            # fetched, we would never try to fetch the missing tweets again.
            # To not have missing tweets, we prefer to not save at all when an error occurs but hope that the error will
            # not occur again on the next run of this function so we can fetch and save all tweets.
            return

        # Newer tweets were added earlier than older ones to new_tweets. However, we want to store older tweets first,
        # so we reverse new_tweets.
        new_tweets.reverse()

        for tweet in new_tweets:
            tweet.save()
            tweet.hashtags.add(*(tweet_hashtag_mappings.get(tweet.tweet_id, [])))
            tweet.save()

        if last_known_tweet_id:
            self.last_known_tweet_id = last_known_tweet_id
            self.save()

        utils.unlock_twitter()


class Hashtag(models.Model):
    hashtag_text = models.CharField(max_length=50, unique=True)
    events = models.ManyToManyField(Event, blank=True, related_name="hashtags")

    def __repr__(self):
        return '<Hashtag %s>' % self.hashtag_text

    def __str__(self):
        return self.hashtag_text

    def clean(self):
        # Twitter treats all hashtags independent of lowercase/uppcase equally.
        # However, moderators might introduce different hashtags by using case uncarefully
        self.hashtag_text = self.hashtag_text.lower()

        # remove leading #
        if self.hashtag_text.startswith('#'):
            self.hashtag_text = self.hashtag_text[1:]


class Tweet(models.Model):
    tweet_id = UnsignedBigIntegerField(unique=True)
    content = models.CharField(max_length=560)
    account = models.ForeignKey(TwitterAccount, on_delete=models.CASCADE)
    hashtags = models.ManyToManyField(Hashtag)
    created_at = models.DateTimeField(default=datetime.now)
    is_reply = models.BooleanField(default=False)

    def __repr__(self):
        date = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return '<Tweet from %s at %s>' % (self.account, date)

    def __str__(self):
        date = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return "%s at %s - %s" % (self.account, date, self.content)
