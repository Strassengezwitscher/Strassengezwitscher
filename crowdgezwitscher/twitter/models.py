from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

from datetime import datetime
import time

from twitter import utils
from crowdgezwitscher.log import logger
from events.models import Event
from TwitterAPI import TwitterAPI, TwitterConnectionError


@python_2_unicode_compatible
class TwitterAccount(models.Model):
    name = models.CharField(max_length=15, unique=True)
    account_id = models.CharField(max_length=20, unique=True)
    last_known_tweet_id = models.CharField(max_length=20, default=0)
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
        if 'id_str' in user:
            self.account_id = user['id_str']
        else:
            logger.warning("Could not find user with provided name.")
            raise ValidationError("Could not find user with provided name.")

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

        return twitter.request('statuses/user_timeline',request_parameters).json()

    def _get_utc_offset(self, twitter):
        tweets = self._fetch_tweets_from_api(twitter, None, None, 1, False)
        if len(tweets) > 0:
            return tweets[0]['user']['utc_offset']

    def fetch_tweets(self):
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
            tweets_from_api = self._fetch_tweets_from_api(twitter, since_id=self.last_known_tweet_id)
            if tweets_from_api:
                last_known_tweet_id = int(tweets_from_api[0]['id_str'])
            while tweets_from_api:
                for tweet_from_api in tweets_from_api:
                    # check if received tweet is already in DB.
                    # if so, break, as we already have all following tweets (Twitter sends newest tweets first)
                    if int(tweet_from_api['id_str']) <= int(self.last_known_tweet_id):
                        should_brake = True
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
                    is_reply = tweet_from_api["in_reply_to_user_id_str"] is not None
                    tweet = Tweet(tweet_id=tweet_from_api['id_str'],
                                  content=tweet_from_api['text'],
                                  created_at=created_at,
                                  is_reply=is_reply,
                                  account=self)
                    new_tweets.append(tweet)
                    hashtags = []
                    for hashtag_from_api in tweet_from_api['entities']['hashtags']:
                        hashtag_text = hashtag_from_api['text']
                        hashtag, _ = Hashtag.objects.get_or_create(hashtag_text=hashtag_text)
                        hashtags.append(hashtag)
                    tweet_hashtag_mappings[tweet.tweet_id] = hashtags
                if should_brake:
                    break
                tweets_from_api = self._fetch_tweets_from_api(
                    twitter,
                    max_id=int(tweets_from_api[-1]['id_str']) - 1)
        except TwitterConnectionError:
            logger.warning("Could not connect to Twitter.")
        except KeyError:
            logger.warning("Got unexpected result while fetching tweets.")
            utils.unlock_twitter()
            return

        new_tweets.reverse()

        for tweet in new_tweets:
            tweet.save()
            tweet.hashtags.add(*(tweet_hashtag_mappings.get(tweet.tweet_id, [])))
            tweet.save()

        if last_known_tweet_id:
            self.last_known_tweet_id = str(last_known_tweet_id)
            self.save()

        utils.unlock_twitter()


@python_2_unicode_compatible
class Hashtag(models.Model):
    hashtag_text = models.CharField(max_length=50, unique=True)
    events = models.ManyToManyField(Event, blank=True, related_name="hashtags")

    def __repr__(self):
        return '<Hashtag %s>' % self.hashtag_text

    def __str__(self):
        return self.hashtag_text

    def clean(self):
        # remove leading #
        if self.hashtag_text.startswith('#'):
            self.hashtag_text = self.hashtag_text[1:]


@python_2_unicode_compatible
class Tweet(models.Model):
    tweet_id = models.CharField(max_length=20, unique=True)
    content = models.CharField(max_length=250)
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
