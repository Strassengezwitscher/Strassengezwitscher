from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.db import IntegrityError
from django.dispatch import receiver

from crowdgezwitscher.log import logger
from TwitterAPI import TwitterAPI, TwitterConnectionError

@python_2_unicode_compatible
class TwitterAccount(models.Model):
    name = models.CharField(max_length=15, unique=True)
    account_id = models.IntegerField(unique=True)
    last_known_tweet_id = models.CharField(max_length=20)

    def __repr__(self):
        return '<TwitterAccount %s>' % self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('twitter:detail', kwargs={'pk': self.pk})

    # Should this happen in the save method?
    def clean(self):
        if self.account_id is None:
            twitter = TwitterAPI(settings.TWITTER_CONSUMER_KEY,
                         settings.TWITTER_CONSUMER_SECRET,
                         auth_type='oAuth2')
            try:
                user = twitter.request('users/lookup', {'screen_name': self.name}).json()[0]
            except TwitterConnectionError:
                logger.warning("Could not connect to Twitter.")
                raise ValidationError("Could not connect to Twitter to retrieve user_id.")
            try :
                self.account_id = user["id"]
            except KeyError:
                logger.warning("Could not get user_id from Twitter response.")
                raise ValidationError("Could not retrieve user_id from Twitter response.")

    def save(self, *args, **kwargs):
        super(TwitterAccount, self).save(*args, **kwargs)
        tweetsCrawled = 0
        twitter = TwitterAPI(settings.TWITTER_CONSUMER_KEY,
                            settings.TWITTER_CONSUMER_SECRET,
                            auth_type='oAuth2')
        try:
            tweets = twitter.request('statuses/user_timeline', {'count': 200, 'user_id': self.account_id,
                                    'trim_user': True, 'exclude_replies': True, 'contributor_details': False}).json()
            if len(tweets) > 0:
                self.last_known_tweet_id = tweets[0]['id_str']
                super(TwitterAccount, self).save(*args, **kwargs)
            while len(tweets) > 0:
                for tweet in tweets:
                    tweetsCrawled += 1
                    tweetObj = Tweet.objects.create_tweet(tweet['id_str'], tweet['text'], self)
                    for hashtag in tweet['entities']['hashtags']:
                        hashtag, _ = Hashtag.objects.get_or_create(hashtag_text=hashtag['text'])
                        tweetObj.hashtags.add(hashtag)
                    tweetObj.save()
                print "%i tweets crawled - now max_id=%s" % (tweetsCrawled, tweets[-1]['id_str'])
                try:
                    tweets = twitter.request('statuses/user_timeline', {'count': 200, 'user_id': self.account_id,
                                            'trim_user': True, 'exclude_replies': True, 'contributor_details': False,
                                            'max_id': int(tweets[-1]['id_str']) - 1}).json()
                except TwitterConnectionError:
                    # complete rollback here
                    logger.warning("Could not connect to Twitter.")
        except TwitterConnectionError:
            # complete rollback here
            logger.warning("Could not connect to Twitter.")
    
# @receiver(post_save, sender=TwitterAccount, dispatch_uid="get_tweets")
# def get_tweets(sender, instance, **kwargs):
    

class HashtagManager(models.Manager):
    def create_hashtag(self, hashtag_text):
        hashtag = self.create(hashtag_text=hashtag_text)
        return hashtag

@python_2_unicode_compatible
class Hashtag(models.Model):
    hashtag_text = models.CharField(max_length=50, unique=True)

    objects = HashtagManager()

    def __str__(self):
        return self.hashtag_text


class TweetManager(models.Manager):
    def create_tweet(self, tweet_id, content, account):
        tweet = self.create(tweet_id=tweet_id, content=content, account=account)
        return tweet

@python_2_unicode_compatible
class Tweet(models.Model):
    tweet_id = models.CharField(max_length=20, unique=True)
    content = models.CharField(max_length=250)
    account = models.ForeignKey(TwitterAccount, on_delete=models.CASCADE)
    hashtags = models.ManyToManyField(Hashtag)

    objects = TweetManager()

    def __str__(self):
        return "%s - %s" % (self.account, self.content)