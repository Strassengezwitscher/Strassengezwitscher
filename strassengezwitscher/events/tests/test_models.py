# pylint: disable=invalid-name,too-many-public-methods
from django.test import TestCase

from events.models import Event


class EventModelTests(TestCase):
    def test_representation(self):
        event = Event(name='Test')
        self.assertEqual(repr(event), '<Event Test>')

    def test_string_representation(self):
        event = Event(name='Test')
        self.assertEqual(str(event), 'Test')
