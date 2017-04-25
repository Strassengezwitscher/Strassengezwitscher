import json

from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase

from base.tests.test_api_views import MapObjectApiViewTestTemplate
from events.models import Event


class EventAPIViewTests(APITestCase):
    fixtures = ['events_views_testdata.json', 'twitter_views_testdata']
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
        for attr in ('id', 'name', 'locationLong', 'locationLat', 'date'):
            self.assertTrue(all(attr in obj for obj in events))
        self.assertEqual(len(events), 2)
        self.assertTrue(len(events) < Event.objects.count())

    # GET /api/events/1/
    def test_read_detail_events(self):
        url = reverse('events_api:detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = {
            'id': 1,
            'name': 'Test Event',
            'location': 'Here',
            'date': '2016-07-20',
            'time': '13:37',
            'repetitionCycle': 'unbekannter Rhythmus',
            'type': '',
            'url': '',
            'counterEvent': False,
            'coverage': True,
            'participants': '',
            'notes': '',
            'organizer': 'Person P',
            'attachments': [
                {
                    'name': 'test.pdf',
                    'description': 'I need a pdf icon',
                    'url': '%sevent_attachments/2016/11/20161111-2349_test_g8nbW.pdf' % settings.MEDIA_URL,
                    'thumbnail_url': '%simg/icon_pdf.png' % settings.STATIC_URL
                },
                {
                    'name': 'noext',
                    'description': 'I have no file extension and need a generic icon',
                    'url': '%sevent_attachments/2016/11/20161111-2349_noext_abcde' % settings.MEDIA_URL,
                    'thumbnail_url': '%simg/icon_file.png' % settings.STATIC_URL
                },
                {
                    'name': 'image.PNG',
                    'description': 'I have a jpg-thumbnail and need no special icon',
                    'url': '%sevent_attachments/2016/11/20161111-2349_image_12345.PNG' % settings.MEDIA_URL,
                    'thumbnail_url': '%sevent_attachments/2016/11/20161111-2349_image_67890.thumbnail.jpg' %
                                     settings.MEDIA_URL
                },
            ],
        }
        self.assertEqual(json.loads(response.content.decode("utf-8")), response_json)

    # GET /api/events/1/
    def test_read_detail_events_with_non_public_attachments(self):
        # set all but one attachment's public fields

        event = Event.objects.get(pk=1)
        for att in event.attachments.all():
            if att.id != 1:
                att.public = False
                att.save()
        url = reverse('events_api:detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = {
            'id': 1,
            'name': 'Test Event',
            'location': 'Here',
            'date': '2016-07-20',
            'time': '13:37',
            'repetitionCycle': 'unbekannter Rhythmus',
            'type': '',
            'url': '',
            'counterEvent': False,
            'coverage': True,
            'participants': '',
            'notes': '',
            'organizer': 'Person P',
            'attachments': [
                {
                    'name': 'test.pdf',
                    'description': 'I need a pdf icon',
                    'url': '%sevent_attachments/2016/11/20161111-2349_test_g8nbW.pdf' % settings.MEDIA_URL,
                    'thumbnail_url': '%simg/icon_pdf.png' % settings.STATIC_URL
                },
            ],
        }
        self.assertEqual(json.loads(response.content.decode("utf-8")), response_json)

    # GET /api/events/1000/
    def test_read_detail_not_existant_event(self):
        url = reverse('events_api:detail', kwargs={'pk': 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # GET /api/events/2/
    def test_read_detail_inactive_mapobject(self):
        self.assertFalse(Event.objects.get(pk=2).active)
        url = reverse('events_api:detail', kwargs={'pk': 2})
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

    # GET /api/events/1/tweets
    def test_get_tweets(self):
        url = reverse('events_api:tweets', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # As this view combines quite some data, this tests needs some documenentation.
        # Please update it if you change the fixtures.
        #
        # The event is limited to the hashtags "wow" and "awesome".
        # Only tweets from 2016-07-24 until 2016-07-25 are considered.
        # The event is limited to the twitter accounts "streetcoverage", "inglor.basterds" and "stalingrad42".
        # There are 3 tweets, each from one of the accounts with at least one of the specified hashtags and within the
        # creation date range:
        response_json = ['11', '22', '66']
        self.assertEqual(sorted(json.loads(response.content.decode("utf-8"))), sorted(response_json))

    # GET /api/events/1000/tweets
    def test_get_tweets_not_existant_event(self):
        url = reverse('events_api:tweets', kwargs={'pk': 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # GET /api/events/2/tweets
    def test_get_tweets_inactive_event(self):
        url = reverse('events_api:tweets', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # GET /api/events/3/tweets
    def test_get_tweets_no_coverage_event(self):
        url = reverse('events_api:tweets', kwargs={'pk': 3})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content.decode("utf-8")), [])

    # POST /api/events/1/tweets
    def test_get_tweets_post_request(self):
        url = reverse('events_api:tweets', kwargs={'pk': 1})
        data = {
            'id': '1',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class EventFilterAPIViewTests(APITestCase, MapObjectApiViewTestTemplate):
    fixtures = ['events_views_testdata.json']
    model = Event

    #
    # Position filter tests
    #

    def test_empty_filter(self):
        url = reverse('events_api:list')
        super(EventFilterAPIViewTests, self).test_empty_filter(url)

    def test_partial_filter(self):
        url = reverse('events_api:list')
        super(EventFilterAPIViewTests, self).test_partial_filter(url)

    def test_no_numbers_filter(self):
        url = reverse('events_api:list')
        super(EventFilterAPIViewTests, self).test_no_numbers_filter(url)

    def test_invalid_numbers_filter(self):
        url = reverse('events_api:list')
        super(EventFilterAPIViewTests, self).test_invalid_numbers_filter(url)

    def test_correct_filter(self):
        url = reverse('events_api:list')
        rect_params = {
            'min_lat': 41.941380,
            'min_long': 72.467309,
            'max_lat': 51.267301,
            'max_long': 99.713402,
        }
        super(EventFilterAPIViewTests, self).test_correct_filter(url, rect_params)

    #
    # Date filter tests
    #

    def test_from_filter(self):
        url = '%s?from=2016-07-13' % reverse('events_api:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        events = response.data
        self.assertEqual(len(events), 2)

    def test_to_filter(self):
        url = '%s?o=2016-07-17' % reverse('events_api:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        events = response.data
        self.assertEqual(len(events), 2)

    def test_from_and_to_filter(self):
        url = '%s?from=2016-07-13&to=2016-07-17' % reverse('events_api:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        events = response.data
        self.assertEqual(len(events), 1)

    def test_from_filter_invalid_format(self):
        url = '%s?from=2016_07_13' % reverse('events_api:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_to_filter_invalid_format(self):
        url = '%s?to=2016_07_17' % reverse('events_api:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
