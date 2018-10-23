from datetime import datetime
from unittest import mock

from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError
from TwitterAPI import TwitterAPI, TwitterConnectionError, TwitterResponse

from twitter.models import Hashtag, TwitterAccount, Tweet


class HashtagModelTests(TestCase):
    def test_representation(self):
        hashtag = Hashtag(hashtag_text='crowdgezwitscher')
        self.assertEqual(repr(hashtag), '<Hashtag crowdgezwitscher>')

    def test_string_representation(self):
        hashtag = Hashtag(hashtag_text='crowdgezwitscher')
        self.assertEqual(str(hashtag), 'crowdgezwitscher')

    # Tests removing of a potentially leading # and enforcing of lowercase hashtags
    def test_clean(self):
        hashtag = Hashtag(hashtag_text='#nyetMyPresident')
        hashtag.clean()
        self.assertEqual(hashtag.hashtag_text, 'nyetmypresident')


class TweetModelTests(TestCase):
    def test_representation(self):
        twitter_account = TwitterAccount(name='Peter')
        tweet = Tweet(content='Erster Tweet, #cool!',
                      created_at=datetime(2012, 12, 21, 19, 9, 0),
                      account=twitter_account,
                      )
        self.assertEqual(repr(tweet), '<Tweet from Peter at 2012-12-21 19:09:00>')

    def test_string_representation(self):
        twitter_account = TwitterAccount(name='Peter')
        tweet = Tweet(content='Erster Tweet, #cool!',
                      created_at=datetime(2012, 12, 21, 19, 9, 0),
                      account=twitter_account,
                      )
        self.assertEqual(str(tweet), 'Peter at 2012-12-21 19:09:00 - Erster Tweet, #cool!')


class MockProcess(object):
    def __init__(self, target):
        self.func = target

    def start(self):
        self.func()

    def is_alive(self):
        return False

    def skip(*args, **kwargs):
        pass

    terminate = join = skip


class TwitterAccountModelTests(TestCase):
    def test_representation(self):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        self.assertEqual(repr(twitter_account), '<TwitterAccount Strassengezwitscher>')

    def test_string_representation(self):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        self.assertEqual(str(twitter_account), 'Strassengezwitscher')

    def test_get_absolute_url(self):
        twitter_account = TwitterAccount(name='PeterTheUnique', account_id=1337)
        twitter_account.save()
        self.assertEqual(twitter_account.get_absolute_url(), '/intern/twitter_accounts/1/')

    @mock.patch('multiprocessing.Process', MockProcess)
    @mock.patch('twitter.utils.lock_twitter', mock.Mock(return_value=True))
    @mock.patch('twitter.models.TwitterAccount._get_utc_offset', mock.Mock(return_value=3600))
    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('twitter.models.TwitterAccount._fetch_tweets_from_api', mock.Mock(side_effect=[[
        {
            'id': 1234,
            'created_at': 'Wed Aug 29 17:12:58 +0000 2012',
            'in_reply_to_user_id': None,
            'full_text': 'Hallo, so ein toller Tweet!',
            'entities': {
                'hashtags': [
                    {
                        'text': 'Hashtag1'
                    },
                    {
                        'text': 'Hashtag2'
                    }
                ]
            }
        },
        {
            'id': 1235,
            'created_at': 'Wed Aug 29 17:14:59 +0000 2012',
            'in_reply_to_user_id': None,
            'full_text': 'Hey, wie toll ist dieser Tweet?',
            'entities': {
                'hashtags': [
                    {
                        'text': 'hashtag2'
                    },
                    {
                        'text': 'Hashtag3'
                    }
                ]
            }
        },
    ], []]))
    def test_complete_tweets_including_hashtags(self):
        twitter_account = TwitterAccount.objects.create(name="Strassengezwitscher", account_id=1337)
        twitter_account.fetch_tweets()
        self.assertEqual(Tweet.objects.count(), 2)
        self.assertEqual(Hashtag.objects.count(), 3)
        self.assertTrue(all([tweet.account == twitter_account for tweet in Tweet.objects.all()]))

    @mock.patch('multiprocessing.Process', MockProcess)
    @mock.patch('twitter.utils.lock_twitter', mock.Mock(return_value=True))
    @mock.patch('twitter.models.TwitterAccount._get_utc_offset', mock.Mock(return_value=3600))
    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('twitter.models.TwitterAccount._fetch_tweets_from_api', mock.Mock(side_effect=[[{
        'id': 1234,
        'created_at': '29 Wed 2012 Aug 17:12:58 +0000'
    }], []]))
    @mock.patch('crowdgezwitscher.log.logger.warning')
    def test_error_during_parsing_creation_time_gets_caught(self, logger):
        twitter_account = TwitterAccount.objects.create(name="Strassengezwitscher", account_id=1337)
        twitter_account.fetch_tweets()
        logger.assert_called_once_with('Got unexpected result while fetching tweets and parsing their creation times.')

    @mock.patch('multiprocessing.Process', MockProcess)
    @mock.patch('twitter.utils.lock_twitter', mock.Mock(return_value=True))
    @mock.patch('twitter.models.TwitterAccount._get_utc_offset', mock.Mock(return_value=3600))
    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('twitter.models.TwitterAccount._fetch_tweets_from_api', mock.Mock(side_effect=[[{
        'id': 9}], []]))
    def test_fetch_tweets_tweet_already_in_db(self):
        twitter_account = TwitterAccount(name="Strassengezwitscher", account_id=1337)
        twitter_account.last_known_tweet_id = 10
        twitter_account.save()
        twitter_account.fetch_tweets()
        self.assertEqual(twitter_account.tweet_set.count(), 0)

    @mock.patch('multiprocessing.Process', MockProcess)
    @mock.patch('twitter.utils.lock_twitter', mock.Mock(return_value=True))
    @mock.patch('twitter.models.TwitterAccount._get_utc_offset', mock.Mock(return_value=3600))
    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('twitter.models.TwitterAccount._fetch_tweets_from_api', mock.Mock(side_effect=[[{
        'id': 1234,
        'created_at': 'Wed Aug 29 17:12:58 +0000 2012',
        'in_reply_to_user_id': None,
        'full_text': 'Hallo, so ein toller Tweet!',
        'entities': {
            'hashtags': []
        }
    }], []]))
    def test_last_known_tweet_id_changes(self):
        twitter_account = TwitterAccount.objects.create(name="Strassengezwitscher", account_id=1337)
        last_known_tweet_id_old = twitter_account.last_known_tweet_id
        twitter_account.fetch_tweets()
        self.assertNotEqual(twitter_account.last_known_tweet_id, last_known_tweet_id_old)
        self.assertEqual(twitter_account.last_known_tweet_id, 1234)

    @mock.patch('multiprocessing.Process', MockProcess)
    @mock.patch('twitter.utils.lock_twitter', mock.Mock(return_value=True))
    @mock.patch('twitter.models.TwitterAccount._get_utc_offset', mock.Mock(return_value=3600))
    @mock.patch('twitter.models.TwitterAccount._fetch_tweets_from_api', mock.Mock(return_value=[{'id': 1234}]))
    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('twitter.utils.unlock_twitter')
    def test_fetch_tweets_unlocks_if_success(self, unlock_mock):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        twitter_account.fetch_tweets()
        self.assertEqual(unlock_mock.call_count, 1)

    @mock.patch('multiprocessing.Process', MockProcess)
    @mock.patch('twitter.utils.lock_twitter', mock.Mock(return_value=True))
    @mock.patch('twitter.models.TwitterAccount._get_utc_offset',
                mock.Mock(side_effect=KeyError("wow, much error, such bad")))
    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('twitter.utils.unlock_twitter')
    @mock.patch('crowdgezwitscher.log.logger.warning')
    def test_fetch_tweets_unlocks_if_get_utc_offset_throws_key_error(self, logger, unlock_mock):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        twitter_account.fetch_tweets()
        logger.assert_called_once_with("Got unexpected result while fetching tweets.")
        self.assertEqual(unlock_mock.call_count, 1)

    @mock.patch('multiprocessing.Process', MockProcess)
    @mock.patch('twitter.utils.lock_twitter', mock.Mock(return_value=True))
    @mock.patch('twitter.models.TwitterAccount._get_utc_offset',
                mock.Mock(side_effect=TwitterConnectionError("wow, much error, such bad")))
    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('twitter.utils.unlock_twitter')
    @mock.patch('crowdgezwitscher.log.logger.warning')
    def test_fetch_tweets_unlocks_if_get_utc_offset_throws_connection_error(self, logger, unlock_mock):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        twitter_account.fetch_tweets()
        logger.assert_called_once_with("Could not connect to Twitter.")
        self.assertEqual(unlock_mock.call_count, 1)

    @mock.patch('multiprocessing.Process', MockProcess)
    @mock.patch('twitter.utils.lock_twitter', mock.Mock(return_value=True))
    @mock.patch('twitter.models.TwitterAccount._get_utc_offset',
                mock.Mock(side_effect=Exception("wow, much error, such bad")))
    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('twitter.utils.unlock_twitter')
    @mock.patch('crowdgezwitscher.log.logger.warning')
    def test_fetch_tweets_unlocks_if_get_utc_offset_throws_unknown_error(self, logger, unlock_mock):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        twitter_account.fetch_tweets()
        logger.assert_called_once_with(
            "Got unexpected exception while fetching tweets: <class 'Exception'> - wow, much error, such bad")
        self.assertEqual(unlock_mock.call_count, 1)

    @mock.patch('twitter.models.TwitterAccount._fetch_tweets_from_api', mock.Mock(return_value=[]))
    def test_get_utc_offset_to_return_nothing_on_no_tweets(self):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        self.assertEqual(twitter_account._get_utc_offset(None), None)

    @mock.patch('twitter.models.TwitterAccount._fetch_tweets_from_api',
                mock.Mock(return_value=[{'user': {'utc_offset': 3600}}]))
    def test_get_utc_offset_to_return_correctly(self):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        self.assertEqual(twitter_account._get_utc_offset(None), 3600)

    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('TwitterAPI.TwitterAPI.request')
    def test_fetch_tweets_from_api_max_since_id_none(self, request_mock):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        twitter = TwitterAPI('a', 'b', auth_type='oAuth2')
        twitter_account._fetch_tweets_from_api(twitter)
        self.assertEqual('since_id' in request_mock.call_args[0][1], False)
        self.assertEqual('max_id' in request_mock.call_args[0][1], False)

    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('TwitterAPI.TwitterAPI.request')
    def test_fetch_tweets_from_api_max_since_id_set(self, request_mock):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        twitter = TwitterAPI('a', 'b', auth_type='oAuth2')
        twitter_account._fetch_tweets_from_api(twitter, max_id=99, since_id=17)
        self.assertEqual('since_id' in request_mock.call_args[0][1], True)
        self.assertEqual('max_id' in request_mock.call_args[0][1], True)

    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('TwitterAPI.TwitterAPI.request',
                mock.Mock(side_effect=TwitterConnectionError("wow, much error, such bad")))
    def test_clean_raises_validation_error_on_twitter_connection_error(self):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        self.assertRaisesMessage(ValidationError,
                                 'Could not connect to Twitter to retrieve user_id.',
                                 twitter_account.clean)

    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('TwitterAPI.TwitterAPI.request')
    @mock.patch('requests.Response.json', mock.Mock(return_value={"not_id": 1}))
    def test_clean_raises_validation_error_on_user_not_found(self, _):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        self.assertRaisesMessage(ValidationError, 'Could not find user with provided name.', twitter_account.clean)

    def mocked_requests_get(*args):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        if args[1] == 'users/show':
            r = MockResponse({'id': 1337}, 200)
            return TwitterResponse(r, None)

    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('TwitterAPI.TwitterAPI.request', mocked_requests_get)
    def test_clean_removes_leading_at(self):
        twitter_account = TwitterAccount(name="@Strassengezwitscher")
        twitter_account.clean()
        self.assertEqual(twitter_account.name, "Strassengezwitscher")

    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('TwitterAPI.TwitterAPI.request', mocked_requests_get)
    def test_clean_adds_account_id(self):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        twitter_account.clean()
        self.assertEqual(twitter_account.account_id, 1337)

    @mock.patch('multiprocessing.Process', MockProcess)
    @mock.patch('twitter.utils.lock_twitter', mock.Mock(return_value=False))
    @mock.patch('TwitterAPI.TwitterAPI.__init__')
    def test_fetch_tweets_returns_after_cannot_acquire_lock(self, mock_twitter_init):
        twitter_account = TwitterAccount(name="Strassengezwitscher")
        twitter_account.fetch_tweets()
        # ToDo: This is not optimal, but I don't know of any better way to ensure that the body of fetch_tweets was not
        # executed
        self.assertFalse(mock_twitter_init.called)

    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('TwitterAPI.TwitterAPI.request', mocked_requests_get)
    def test_add_account_with_same_name_but_different_capitalization(self):
        TwitterAccount.objects.create(name="Strassengezwitscher", account_id=1337)
        twitter_account_new = TwitterAccount(name="STRASSENGEZWITSCHER")

        self.assertRaisesMessage(ValidationError, 'Twitter account with this name already exists.', twitter_account_new.clean)


class TwitterAccountModelTransactionTests(TransactionTestCase):
    @mock.patch('multiprocessing.Process', MockProcess)
    @mock.patch('twitter.utils.lock_twitter', mock.Mock(return_value=True))
    @mock.patch('twitter.models.TwitterAccount._get_utc_offset', mock.Mock(return_value=3600))
    @mock.patch('twitter.models.TwitterAccount._fetch_tweets_from_api', mock.Mock(side_effect=[[
        {
            'id': 1234,
            'created_at': 'Wed Aug 29 17:12:58 +0000 2012',
            'in_reply_to_user_id': None,
            'full_text': 'wow, much inconsistency, such duplication',
            'entities': {
                'hashtags': []
            }
        },
    ], []]))
    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('crowdgezwitscher.log.logger.warning')
    def test_reset_last_known_tweet_id(self, logger):
        twitter_account = TwitterAccount.objects.create(name="Strassengezwitscher", account_id=1)
        Tweet.objects.create(
            tweet_id=1234,
            content="I will be fetched even though I am already in the DB",
            account=twitter_account,
        )
        tweet_count_old = twitter_account.tweet_set.count()

        twitter_account.fetch_tweets()
        tweet_count_new = twitter_account.tweet_set.count()
        self.assertEqual(tweet_count_old, tweet_count_new)
        self.assertEqual(logger.call_count, 1)
        self.assertEqual(twitter_account.last_known_tweet_id, 1234)
