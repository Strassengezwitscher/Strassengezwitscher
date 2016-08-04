from django.urls import reverse
from django.test import TestCase

from strassengezwitscher.models import MapObject


class StrassengezwitscherTests(TestCase):
    def test_serves_angular_tag(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<sg-app>', response.content)
        self.assertIn(b'</sg-app>', response.content)


class MapObjectModelTests(TestCase):
    def test_representation(self):
        obj = MapObject(name='Test')
        self.assertEqual(repr(obj), '<MapObject Test>')

    def test_string_representation(self):
        obj = MapObject(name='Test')
        self.assertEqual(str(obj), 'Test')
