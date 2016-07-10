import json
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from mapobjects.models import MapObject


class MapObjectViewTests(APITestCase):

    fixtures = ['initial_mapobjects.json']

    #
    # test correct behavior for all CRUD operations (CREATE, READ, UPDATE, DELETE)
    # via all possible HTTP methods (POST, GET, PATCH, PUT, DELETE)
    # on mapobject list ("/mapobjects/"") and detail(e.g."/mapobjects/1/")

    # POST /mapobjects/
    def test_create_list_mapobject(self):
        url = reverse('mapobjects:list')
        data = {
            'id': '1',
            'name': 'Amsterdaaaaaaaaaaaaaaaaam',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # POST /mapobjects/1/
    def test_create_detail_mapobject(self):
        url = reverse('mapobjects:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'name': 'Amsterdaaaaaaaaaaaaaaaaam',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # GET /mapobjects/
    def test_read_list_mapobject(self):
        url = reverse('mapobjects:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MapObject.objects.count(), 4)

    # GET /mapobjects/1/
    def test_read_detail_mapobject(self):
        url = reverse('mapobjects:detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = {
            u'id': 1,
            u'active': True,
            u'name': u'Amsterdam1',
            u'location': u'Amsterdam',
            u'locationLong': u'4.894045',
            u'locationLat': u'52.368829'
        }
        self.assertEqual(json.loads(response.content.decode("utf-8")), response_json)

    # PATCH /mapobjects/
    def test_modify_list_mapobject(self):
        url = reverse('mapobjects:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'name': 'Amsterdaaaaaaaaaaaaaaaaam',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # PATCH /mapobjects/1/
    def test_modify_detail_mapobject(self):
        url = reverse('mapobjects:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'name': 'Amsterdaaaaaaaaaaaaaaaaam',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # PUT /mapobjects/
    def test_replace_list_mapobject(self):
        url = reverse('mapobjects:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'name': 'Amsterdaaaaaaaaaaaaaaaaam',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # PUT /mapobjects/1/
    def test_replace_detail_mapobject(self):
        url = reverse('mapobjects:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'name': 'Amsterdaaaaaaaaaaaaaaaaam',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # DELETE /mapobjects/
    def test_delete_list_mapobject(self):
        url = reverse('mapobjects:list')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # DELETE /mapobjects/1/
    def test_delete_detail_mapobject(self):
        url = reverse('mapobjects:detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # Test correct json urls
    # GET /mapobjects.json
    def test_json_list_mapobject(self):
        url = '/api/mapobjects.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # GET /mapobjects/.json
    def test_json_list_mapobject_incorrect(self):
        url = '/api/mapobjects/.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # GET /mapobjects/1.json
    def test_json_detail_mapobject(self):
        url = '/api/mapobjects/1.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # GET /mapobjects1.json
    def test_json_detail_mapobject_incorrect(self):
        url = '/api/mapobjects1.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
