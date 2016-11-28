import json

import mock
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase
from TwitterAPI import TwitterResponse, TwitterConnectionError

from events.models import Event
from crowdgezwitscher.tests.test_api_views import MapObjectApiViewTestTemplate


class EventAPIViewTests(APITestCase):
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
            u'id': 1,
            u'name': u'Test Event',
            u'location': u'Here',
            u'date': u'2016-07-20',
            u'repetitionCycle': u'unbekannter Rhythmus',
            u'type': u'',
            u'url': u'',
            u'counterEvent': False,
            u'coverage': True,
            u'participants': u'',
            u'organizer': u'Person P',
            u'attachments': [
                {'name': u'test.pdf',
                 'description': u'I can haz description',
                 'url': u'%sevent_attachments/2016/11/20161111-2349_test_g8nbW.pdf' % settings.MEDIA_URL,
                 'thumbnail_url': u'%simg/icon_pdf.png' % settings.STATIC_URL},
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

    def mock_twitter_rest_api_search_tweets(*args, **kwargs):
        return [{'id_str': '123'}, {'id_str': '456'}]

    def mock_twitter_rest_api_search_tweets_missing_field(*args, **kwargs):
        return [{'foo': 'bar'}, {'id_str': '456'}]

    def mock_twitter_rest_api_search_tweets_connection_error(*args, **kwargs):
        raise TwitterConnectionError("wow, much error, such bad")

    def mock_twitter_rest_api_search_tweets_rate_limit_exhausted(*args, **kwargs):
        m = mock.Mock()
        m.status_code = 429  # Twitter uses 429 for exhausted rate limits
        return TwitterResponse(m, None)

    def mock_twitter_rest_api_search_tweets_some_error(*args, **kwargs):
        m = mock.Mock()
        m.status_code = 500  # just some error we do not handle specifically
        return TwitterResponse(m, None)

    # GET /api/events/1/tweets
    @mock.patch('TwitterAPI.TwitterAPI.__init__', lambda *args, **kwargs: None)
    @mock.patch('TwitterAPI.TwitterAPI.request', mock_twitter_rest_api_search_tweets)
    def test_get_tweets(self):
        url = reverse('events_api:tweets', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ['123', '456'])

    def test_get_tweets_coverage_disabled(self):
        url = reverse('events_api:tweets', kwargs={'pk': 3})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    @mock.patch('TwitterAPI.TwitterAPI.request', mock_twitter_rest_api_search_tweets)
    def test_no_tweets_for_misconfigured_event(self):
        pk = 2
        event = Event.objects.get(pk=pk)
        self.assertEqual(type(event), Event)  # just make sure object exists despite returned 404 below
        url = reverse('events_api:tweets', kwargs={'pk': pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data['status'], 'error')
        self.assertTrue('improperly configured' in response.data['errors'])

    @mock.patch('TwitterAPI.TwitterAPI.__init__', lambda *args, **kwargs: None)
    @mock.patch('TwitterAPI.TwitterAPI.request', mock_twitter_rest_api_search_tweets_missing_field)
    def test_twitter_unexpected_answer(self):
        url = reverse('events_api:tweets', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ['456'])

    @mock.patch('TwitterAPI.TwitterAPI.__init__', lambda *args, **kwargs: None)
    @mock.patch('TwitterAPI.TwitterAPI.request', mock_twitter_rest_api_search_tweets_connection_error)
    def test_twitter_connection_error(self):
        url = reverse('events_api:tweets', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    @mock.patch('TwitterAPI.TwitterAPI.__init__', lambda *args, **kwargs: None)
    @mock.patch('TwitterAPI.TwitterAPI.request', mock_twitter_rest_api_search_tweets_rate_limit_exhausted)
    def test_twitter_rate_limit_exceeded(self):
        url = reverse('events_api:tweets', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    @mock.patch('TwitterAPI.TwitterAPI.__init__', lambda *args, **kwargs: None)
    @mock.patch('TwitterAPI.TwitterAPI.request', mock_twitter_rest_api_search_tweets_some_error)
    def test_twitter_some_error(self):
        url = reverse('events_api:tweets', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

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
            'max_long': 99.713402
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
