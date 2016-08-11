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
