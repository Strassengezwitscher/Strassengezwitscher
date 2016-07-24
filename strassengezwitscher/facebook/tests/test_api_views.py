import json
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from facebook.models import FacebookPage


class FacebookPageAPIViewTests(APITestCase):

    fixtures = ['facebook_views_testdata.json']

    #
    # test correct behavior for all CRUD operations (CREATE, READ, UPDATE, DELETE)
    # via all possible HTTP methods (POST, GET, PATCH, PUT, DELETE)
    # on mapobject list ("/api/facebook/") and detail(e.g."/api/facebook/1/")

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
    def test_read_list_mapobject(self):
        url = reverse('facebook_api:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FacebookPage.objects.count(), 2)

    # GET /api/facebook/1/
    def test_read_detail_mapobject(self):
        url = reverse('facebook_api:detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = {
            u'id': 1,
            u'active': True,
            u'name': u'Test page',
            u'location': u'Nowhere',
            u'locationLat': u'12.345000',
            u'locationLong': u'54.321000',
        }
        self.assertEqual(json.loads(response.content.decode("utf-8")), response_json)

    # PATCH /api/facebook/
    def test_modify_list_facebook(self):
        url = reverse('facebook_api:detail', kwargs={'pk': 1})
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
        url = reverse('facebook_api:detail', kwargs={'pk': 1})
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

    # GET /mapobjects1.json
    def test_json_detail_facebook_incorrect(self):
        url = '/api/facebook1.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
