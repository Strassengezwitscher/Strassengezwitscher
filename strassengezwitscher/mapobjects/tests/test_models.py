from django.test import TestCase

from mapobjects.models import MapObject


class MapObjectModelTests(TestCase):
    def test_representation(self):
        obj = MapObject(name='Test')
        self.assertEqual(repr(obj), '<MapObject Test>')

    def test_string_representation(self):
        obj = MapObject(name='Test')
        self.assertEqual(str(obj), 'Test')
