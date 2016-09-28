import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from blogs.models import BlogEntry


class BlogAPIViewTests(APITestCase):

    fixtures = ['blogs_views_testdata.json', 'users_views_testdata', 'events_views_testdata.json', 'facebook_views_testdata.json']
    model = BlogEntry

    # Test correct behavior for all CRUD operations (CREATE, READ, UPDATE, DELETE)
    # via all possible HTTP methods (POST, GET, PATCH, PUT, DELETE)
    # on list ("/api/blogs/") and detail(e.g."/api/blogs/1/")

    # POST /api/blogs/
    def test_create_list_blogs(self):
        url = reverse('blogs_api:list')
        data = {
            'id': '1',
            'title': 'Test Blog',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # POST /api/blogs/1/
    def test_create_detail_blogs(self):
        url = reverse('blogs_api:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'title': 'Test Blog',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # GET /api/blogs/
    def test_read_list_blogs(self):
        url = reverse('blogs_api:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blogs = response.data
        attributes = ['title', 'content', 'created_by', 'created_on']

        for blog in blogs:
            self.assertTrue(all(blog.get(att) for att in attributes))

        self.assertEqual(len(blogs), 1)
        self.assertTrue(len(blogs) < BlogEntry.objects.count())

    # GET /api/blogs/1/
    def test_read_detail_blogs(self):
        blog_id = 1
        blog_entry = BlogEntry.objects.get(pk=blog_id)
        url = reverse('blogs_api:detail', kwargs={'pk': 1})
        response = self.client.get(url)
        response_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['title'], blog_entry.title)
        self.assertEqual(response_json['created_by'], blog_entry.created_by.get_full_name())
        self.assertEqual(response_json['created_on'], blog_entry.created_on.strftime('%d.%m.%Y'))
        self.assertEqual(response_json['content'], blog_entry.content)

    # GET /api/blogs/1000/
    def test_read_detail_not_existant_mapobject(self):
        url = reverse('blogs_api:detail', kwargs={'pk': 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # GET /api/blogs/3/
    def test_read_detail_draft(self):
        self.assertTrue(BlogEntry.objects.get(pk=2).status == BlogEntry.DRAFT)
        url = reverse('blogs_api:detail', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # PATCH /api/blogs/
    def test_modify_list_blogs(self):
        url = reverse('blogs_api:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'title': 'Test Blog fix',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # PATCH /api/blogs/1/
    def test_modify_detail_blogs(self):
        url = reverse('blogs_api:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'title': 'Test Blog fix',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # PUT /api/blogs/
    def test_replace_list_blogs(self):
        url = reverse('blogs_api:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'title': 'Test Blog fix',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # PUT /api/blogs/1/
    def test_replace_detail_blogs(self):
        url = reverse('blogs_api:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'title': 'Test Blog fix',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # DELETE /api/blogs/
    def test_delete_list_blogs(self):
        url = reverse('blogs_api:list')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # DELETE /api/blogs/1/
    def test_delete_detail_blogs(self):
        url = reverse('blogs_api:detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # Test correct json urls
    # GET /blogs.json
    def test_json_list_blogs(self):
        url = '/api/blogs.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # GET /api/blogs/.json
    def test_json_list_blogs_incorrect(self):
        url = '/api/blogs/.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # GET /api/blogs/1.json
    def test_json_detail_blogs(self):
        url = '/api/blogs/1.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # GET /mapobjects1.json
    def test_json_detail_blogs_incorrect(self):
        url = '/api/blogs1.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
