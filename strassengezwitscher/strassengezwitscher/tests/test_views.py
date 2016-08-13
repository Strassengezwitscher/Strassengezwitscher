from django.urls import reverse
from django.test import TestCase
from rest_framework import status

import json
from decimal import Decimal

class StrassengezwitscherTests(TestCase):
    def test_serves_angular_tag(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<sg-app>', response.content)
        self.assertIn(b'</sg-app>', response.content)

class MapObjectViewTestTemplate(object):

    def test_empty_filter(self, url):
        response = self.client.get(url)
        filtered_objects = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(filtered_objects), self.model.objects.count())

    def test_partial_filter(self, url):
        response = self.client.get(url, {'min_lat': 10.0, 'min_long': 11.0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_numbers_filter(self, url):
        response = self.client.get(url, {'min_lat': 'a', 'min_long': 'b', 'max_lat': 'c', 'max_long': 'd'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_numbers_filter(self, url):
        square_params = {
            'min_lat': -400.0,
            'min_long': -200.0,
            'max_lat': 400.0,
            'max_long': 300.0
        }
        response = self.client.get(url, square_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_correct_filter(self, url, square_params):

        response = self.client.get(url, square_params)
        filtered_objects = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(filtered_objects), 0)
        self.assertLess(len(filtered_objects), self.model.objects.count())

        for o in filtered_objects:
            self.assertGreaterEqual(o['locationLat'], Decimal(square_params['min_lat']))
            self.assertGreaterEqual(o['locationLong'], Decimal(square_params['min_long']))
            self.assertLessEqual(o['locationLat'], Decimal(square_params['max_lat']))
            self.assertLessEqual(o['locationLong'], Decimal(square_params['max_long']))

