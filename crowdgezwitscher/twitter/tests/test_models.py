from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime

import mock
from mock import patch
from twitter import utils
from twitter.models import Hashtag, TwitterAccount, Tweet

from TwitterAPI import TwitterConnectionError, TwitterResponse
import requests


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
        twitter_account = TwitterAccount(name='Peter')
        tweet = Tweet(content='Erster Tweet, #cool!', created_at=datetime(2012, 12, 21, 19, 9, 0), account=twitter_account)
        self.assertEqual(str(tweet), 'Peter at 2012-12-21 19:09:00 - Erster Tweet, #cool!')


class TwitterAccountTests(TestCase):
    def test_representation(self):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        self.assertEqual(repr(twitter_account), '<TwitterAccount Strassengezwitscher>')

    def test_string_representation(self):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        self.assertEqual(str(twitter_account), 'Strassengezwitscher')

    def mock_twitter_request_users_show_connection_error(*args, **kwargs):
        raise TwitterConnectionError("wow, much error, such bad")

    @mock.patch('TwitterAPI.TwitterAPI.__init__', lambda *args, **kwargs: None)
    @mock.patch('TwitterAPI.TwitterAPI.request', mock_twitter_request_users_show_connection_error)
    def test_clean_raises_validation_error_on_twitter_connection_error(self):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        self.assertRaisesMessage(ValidationError, 'Could not connect to Twitter to retrieve user_id.', lambda: twitter_account.clean())

    def mock_response_json(*args, **kwargs):
        return {"not_id_str": '1'}

    @mock.patch('TwitterAPI.TwitterAPI.__init__', lambda *args, **kwargs: None)
    @mock.patch('TwitterAPI.TwitterAPI.request')
    @mock.patch('requests.Response.json', mock_response_json)
    def test_clean_raises_validation_error_on_user_not_found(self, _):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        self.assertRaisesMessage(ValidationError, 'Could not find user with provided name.', lambda: twitter_account.clean())

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        if args[1] == 'users/show':
            r = MockResponse({"id_str": "1337"}, 200)
            return TwitterResponse(r, None)

    @mock.patch('TwitterAPI.TwitterAPI.__init__', lambda *args, **kwargs: None)
    @mock.patch('TwitterAPI.TwitterAPI.request', mocked_requests_get)
    def test_clean_removes_leading_at(self):
        twitter_account = TwitterAccount(name="@Strassengezwitscher")
        twitter_account.clean()
        self.assertEqual(twitter_account.name, "Strassengezwitscher")

    @mock.patch('TwitterAPI.TwitterAPI.__init__', lambda *args, **kwargs: None)
    @mock.patch('TwitterAPI.TwitterAPI.request', mocked_requests_get)
    def test_clean_adds_account_id(self):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        twitter_account.clean()
        self.assertEqual(twitter_account.account_id, "1337")

    def mock_lock_twitter(*args, **kwargs):
        return False

    @mock.patch('twitter.utils.lock_twitter', mock_lock_twitter)
    @mock.patch('TwitterAPI.TwitterAPI.__init__')
    def test_fetch_tweets_returns_after_cannot_acquire_lock(self, mock_twitter_init):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        twitter_account.fetch_tweets()
        # ToDo: This is not optimal, but I don't know of any better way to ensure that the body of fetch_tweets was not executed
        self.assertFalse(mock_twitter_init.called)