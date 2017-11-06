import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from base.tests.test_api_views import MapObjectApiViewTestTemplate
from facebook.models import FacebookPage


class FacebookPageAPIViewTests(APITestCase, MapObjectApiViewTestTemplate):

    fixtures = ['facebook_views_testdata.json']
    model = FacebookPage

    # Test correct behavior for all CRUD operations (CREATE, READ, UPDATE, DELETE)
    # via all possible HTTP methods (POST, GET, PATCH, PUT, DELETE)
    # on list ("/api/facebook/") and detail(e.g."/api/facebook/1/")

    # POST /api/facebook/
    def test_create_list_facebook(self):
        url = reverse('facebook_api:list')
        data = {
            'id': '1',
            'name': 'Test page',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # POST /api/facebook/1/
    def test_create_detail_facebook(self):
        url = reverse('facebook_api:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'name': 'Test page',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # GET /api/facebook/
    def test_read_list_facebook(self):
        url = reverse('facebook_api:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        facebook_pages = response.data
        for attr in ('id', 'name', 'locationLong', 'locationLat'):
            self.assertTrue(all(attr in obj for obj in facebook_pages))
        self.assertEqual(len(facebook_pages), 2)
        self.assertTrue(len(facebook_pages) < FacebookPage.objects.count())

    # GET /api/facebook/1/
    def test_read_detail_facebook(self):
        url = reverse('facebook_api:detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = {
            'id': 1,
            'name': 'Test page',
            'location': 'Nowhere',
            'facebookId': '1',
            'notes': '',
        }
        self.assertEqual(json.loads(response.content.decode("utf-8")), response_json)

    # GET /api/facebook/1000/
    def test_read_detail_not_existant_facebook_page(self):
        url = reverse('facebook_api:detail', kwargs={'pk': 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # GET /api/facebook/3/
    def test_read_detail_inactive_facebook_page(self):
        self.assertFalse(FacebookPage.objects.get(pk=3).active)
        url = reverse('facebook_api:detail', kwargs={'pk': 3})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # PATCH /api/facebook/
    def test_modify_list_facebook(self):
        url = reverse('facebook_api:list')
        data = {
            'id': '1',
            'name': 'Test page fix',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # PATCH /api/facebook/1/
    def test_modify_detail_facebook(self):
        url = reverse('facebook_api:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'name': 'Test page fix',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # PUT /api/facebook/
    def test_replace_list_facebook(self):
        url = reverse('facebook_api:list')
        data = {
            'id': '1',
            'name': 'Test page fix',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # PUT /api/facebook/1/
    def test_replace_detail_facebook(self):
        url = reverse('facebook_api:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'name': 'Test page fix',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # DELETE /api/facebook/
    def test_delete_list_facebook(self):
        url = reverse('facebook_api:list')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # DELETE /api/facebook/1/
    def test_delete_detail_facebook(self):
        url = reverse('facebook_api:detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # Test correct json urls
    # GET /facebook.json
    def test_json_list_facebook(self):
        url = '/api/facebook.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # GET /api/facebook/.json
    def test_json_list_facebook_incorrect(self):
        url = '/api/facebook/.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # GET /api/facebook/1.json
    def test_json_detail_facebook(self):
        url = '/api/facebook/1.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # GET /api/facebook1.json
    def test_json_detail_facebook_incorrect(self):
        url = '/api/facebook1.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    #
    # Test backend filters
    #

    def test_empty_filter(self):
        url = reverse('facebook_api:list')
        super(FacebookPageAPIViewTests, self).test_empty_filter(url)

    def test_partial_filter(self):
        url = reverse('facebook_api:list')
        super(FacebookPageAPIViewTests, self).test_partial_filter(url)

    def test_no_numbers_filter(self):
        url = reverse('facebook_api:list')
        super(FacebookPageAPIViewTests, self).test_no_numbers_filter(url)

    def test_invalid_numbers_filter(self):
        url = reverse('facebook_api:list')
        super(FacebookPageAPIViewTests, self).test_invalid_numbers_filter(url)

    def test_correct_filter(self):
        url = reverse('facebook_api:list')
        rect_params = {
            'min_lat': 53.854762,
            'min_long': 10.656980,
            'max_lat': 55.592905,
            'max_long': 14.084714
        }
        super(FacebookPageAPIViewTests, self).test_correct_filter(url, rect_params)

    #
    # Test receiving of new FB page
    #
    def test_incomplete_data(self):
        """Test sending not all required fields."""
        response = self.client.post(reverse('facebook_api:send_form'),
                                    json.dumps({'facebookId': "foo", 'location': "Dresden",
                                     'locationLong': 52.1,'name':"TestEvent", 'notes': "N"}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')
        self.assertTrue('Fehler beim Speichern der Informationen.' in response.json()['message'])

    def test_valid_data(self):
        """Test sending correct values."""
        response = self.client.post(reverse('facebook_api:send_form'),
                                    json.dumps({'facebookId': "foo", 'location': "Dresden",
                                     'locationLat': 51.3, 'locationLong': 52.1,'name':"TestEvent", 'notes': "N"}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)
