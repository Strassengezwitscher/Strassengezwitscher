from datetime import date

from django.test import TestCase

from events.models import Event


class EventModelTests(TestCase):
    def test_representation(self):
        event = Event(name='Test', date=date(2012, 12, 21), organizer="Organizer")
        self.assertEqual(repr(event), '<Event Test at 2012-12-21 by Organizer>')

    def test_representation_date_only(self):
        event = Event(date=date(2012, 12, 21))
        self.assertEqual(repr(event), '<Event unbenannt at 2012-12-21>')

    def test_representation_date_and_name(self):
        event = Event(name='Test', date=date(2012, 12, 21))
        self.assertEqual(repr(event), '<Event Test at 2012-12-21>')

    def test_representation_date_and_organizer(self):
        event = Event(date=date(2012, 12, 21), organizer="Organizer")
        self.assertEqual(repr(event), '<Event unbenannt at 2012-12-21 by Organizer>')

    def test_string_representation(self):
        event = Event(name='Test', date=date(2012, 12, 21), organizer="Organizer")
        self.assertEqual(str(event), 'Test at 2012-12-21 by Organizer')

    def test_string_representation_date_only(self):
        event = Event(date=date(2012, 12, 21))
        self.assertEqual(str(event), 'unbenannt at 2012-12-21')

    def test_string_representation_date_and_name(self):
        event = Event(name='Test', date=date(2012, 12, 21))
        self.assertEqual(str(event), 'Test at 2012-12-21')

    def test_string_representation_date_and_organizer(self):
        event = Event(date=date(2012, 12, 21), organizer="Organizer")
        self.assertEqual(str(event), 'unbenannt at 2012-12-21 by Organizer')

    def test__is_ready_for_twitter(self):
        event = Event(twitter_account_names='foo,bar', twitter_hashtags='baz,quux', coverage_start=date(2016, 9, 27))
        self.assertFalse(event._is_ready_for_twitter())
        event.coverage_end = date(2016, 9, 28)
        self.assertTrue(event._is_ready_for_twitter())

    def test_build_twitter_search_query(self):
        event = Event(twitter_account_names='foo', coverage_start=date(2016, 9, 27), coverage_end=date(2016, 9, 28))
        self.assertIsNone(event.build_twitter_search_query())
        event.twitter_hashtags = 'baz'
        self.assertEqual(event.build_twitter_search_query(), '#baz from:foo')
        event.twitter_account_names = 'foo, @bar,@foobar'
        event.twitter_hashtags = 'baz,#quux , #bazquux'
        self.assertEqual(event.build_twitter_search_query(),
                         '#baz OR #quux OR #bazquux from:foo OR from:bar OR from:foobar')
