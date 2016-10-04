import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from events.models import Event

from crowdgezwitscher.tests.test_api_views import MapObjectApiViewTestTemplate


class EventAPIViewTests(APITestCase, MapObjectApiViewTestTemplate):

    fixtures = ['events_views_testdata.json']
    model = Event

    # Test correct behavior for all CRUD operations (CREATE, READ, UPDATE, DELETE)
    # via all possible HTTP methods (POST, GET, PATCH, PUT, DELETE)
    # on list ("/api/events/") and detail (e.g."/api/events/1/")

    # POST /api/events/
    def test_create_list_events(self):
        url = reverse('events_api:list')
        data = {
            'id': '1',
            'name': 'Test Event',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # POST /api/events/1/
    def test_create_detail_events(self):
        url = reverse('events_api:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'name': 'Test Event',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # GET /api/events/
    def test_read_list_events(self):
        url = reverse('events_api:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        events = response.data
        for attr in ('id', 'name', 'locationLong', 'locationLat'):
            self.assertTrue(all(attr in obj for obj in events))
        self.assertEqual(len(events), 2)
        self.assertTrue(len(events) < Event.objects.count())

    # GET /api/events/1/
    def test_read_detail_events(self):
        url = reverse('events_api:detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = {
            u'id': 1,
            u'name': u'Test Event',
            u'location': u'Here',
            u'date': u'2016-07-24',
            u'repetitionCycle': u'unbekannter Rhythmus',
            u'type': u'',
            u'url': u'',
            u'counterEvent': False,
            u'coverage': False,
            u'participants': u'',
        }
        self.assertEqual(json.loads(response.content.decode("utf-8")), response_json)

    # GET /api/events/1000/
    def test_read_detail_not_existant_event(self):
        url = reverse('events_api:detail', kwargs={'pk': 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # GET /api/events/3/
    def test_read_detail_inactive_event(self):
        self.assertFalse(Event.objects.get(pk=3).active)
        url = reverse('events_api:detail', kwargs={'pk': 3})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # PATCH /api/events/
    def test_modify_list_events(self):
        url = reverse('events_api:list')
        data = {
            'id': '1',
            'name': 'Test Event fix',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # PATCH /api/events/1/
    def test_modify_detail_events(self):
        url = reverse('events_api:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'name': 'Test Event fix',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # PUT /api/events/
    def test_replace_list_events(self):
        url = reverse('events_api:list')
        data = {
            'id': '1',
            'name': 'Test Event fix',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # PUT /api/events/1/
    def test_replace_detail_events(self):
        url = reverse('events_api:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'name': 'Test Event fix',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # DELETE /api/events/
    def test_delete_list_events(self):
        url = reverse('events_api:list')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # DELETE /api/events/1/
    def test_delete_detail_events(self):
        url = reverse('events_api:detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # Test correct json urls
    # GET /api/events.json
    def test_json_list_events(self):
        url = '/api/events.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # GET /api/events/.json
    def test_json_list_events_incorrect(self):
        url = '/api/events/.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # GET /api/events/1.json
    def test_json_detail_events(self):
        url = '/api/events/1.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # GET /api/events1.json
    def test_json_detail_events_incorrect(self):
        url = '/api/events1.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    #
    # Test backend filters
    #

    def test_empty_filter(self):
        url = reverse('events_api:list')
        super(EventAPIViewTests, self).test_empty_filter(url)

    def test_partial_filter(self):
        url = reverse('events_api:list')
        super(EventAPIViewTests, self).test_partial_filter(url)

    def test_no_numbers_filter(self):
        url = reverse('events_api:list')
        super(EventAPIViewTests, self).test_no_numbers_filter(url)

    def test_invalid_numbers_filter(self):
        url = reverse('events_api:list')
        super(EventAPIViewTests, self).test_invalid_numbers_filter(url)

    def test_correct_filter(self):
        url = reverse('events_api:list')
        rect_params = {
            'min_lat': 41.941380,
            'min_long': 72.467309,
            'max_lat': 51.267301,
            'max_long': 99.713402
        }
        super(EventAPIViewTests, self).test_correct_filter(url, rect_params)
