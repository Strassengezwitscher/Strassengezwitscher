from django.test import TestCase
from datetime import datetime

from twitter.models import Hashtag, TwitterAccount, Tweet


class HashtagModelTests(TestCase):
    def test_string_representation(self):
        hashtag = Hashtag(hashtag_text='crowdgezwitscher')
        self.assertEqual(str(hashtag), 'crowdgezwitscher')

    def test_clean(self):
        hashtag = Hashtag(hashtag_text='#nyetMyPresident')
        hashtag.clean()
        self.assertEqual(hashtag.hashtag_text, 'nyetMyPresident')


class TweetModelTests(TestCase):
    def test_string_representation(self):
        twitteraccount = TwitterAccount(name='Peter')
        tweet = Tweet(content='Erster Tweet, #cool!', created_at=datetime(2012, 12, 21, 19, 9, 0), account=twitteraccount)
        self.assertEqual(str(tweet), 'Peter at 2012-12-21 19:09:00 - Erster Tweet, #cool!')