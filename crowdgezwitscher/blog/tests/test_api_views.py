import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from blog.models import BlogEntry


class BlogAPIViewTests(APITestCase):
    fixtures = ['blog_views_testdata.json', 'users_views_testdata', 'events_views_testdata.json',
                'facebook_views_testdata.json']
    model = BlogEntry

    # Test correct behavior for all CRUD operations (CREATE, READ, UPDATE, DELETE)
    # via all possible HTTP methods (POST, GET, PATCH, PUT, DELETE)
    # on list ("/api/blog/") and detail(e.g."/api/blog/1/")

    # POST /api/blog/
    def test_create_blog_list(self):
        url = reverse('blog_api:list')
        data = {
            'id': '1',
            'title': 'Test Blog',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # POST /api/blog/1/
    def test_create_blogentry(self):
        url = reverse('blog_api:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'title': 'Test Blog Entry',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # GET /api/blog/
    def test_read_blog_list(self):
        url = reverse('blog_api:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blogentries = response.data
        attributes = ['title', 'content', 'created_by', 'created_on']

        for entry in blogentries:
            self.assertTrue(all(entry.get(att) for att in attributes))

        self.assertEqual(len(blogentries), BlogEntry.objects.filter(status=BlogEntry.PUBLISHED).count())
        self.assertTrue(len(blogentries) < BlogEntry.objects.count())

    # GET /api/blog/1/
    def test_read_blogentry(self):
        blog_id = 1
        blogentry = BlogEntry.objects.get(pk=blog_id)
        url = reverse('blog_api:detail', kwargs={'pk': 1})
        response = self.client.get(url)
        response_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['title'], blogentry.title)
        self.assertEqual(response_json['created_by'], blogentry.created_by.get_full_name())
        self.assertEqual(response_json['created_on'], blogentry.created_on.strftime('%d.%m.%Y'))
        self.assertEqual(response_json['content'], blogentry.content)

    # GET /api/blog/1000/
    def test_read_not_existant_blogentry(self):
        url = reverse('blog_api:detail', kwargs={'pk': 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # GET /api/blog/3/
    def test_read_blogentry_draft(self):
        self.assertTrue(BlogEntry.objects.get(pk=2).status == BlogEntry.DRAFT)
        url = reverse('blog_api:detail', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # PATCH /api/blog/
    def test_modify_blog_list(self):
        url = reverse('blog_api:list')
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # PATCH /api/blog/1/
    def test_modify_blogentry(self):
        url = reverse('blog_api:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'title': 'Test Blog fix',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # PUT /api/blog/
    def test_replace_blog_list(self):
        url = reverse('blog_api:list')
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # PUT /api/blog/1/
    def test_replace_blogentry(self):
        url = reverse('blog_api:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'title': 'Test Blog fix',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # DELETE /api/blog/
    def test_delete_blog_list(self):
        url = reverse('blog_api:list')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # DELETE /api/blog/1/
    def test_delete_blogentry(self):
        url = reverse('blog_api:detail', kwargs={'pk': 1})
        data = {
            'id': '1',
            'title': 'Test Blog fix',
        }
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # Test correct json urls
    # GET /blog.json
    def test_json_blog_list(self):
        url = '/api/blog.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # GET /api/blog/.json
    def test_json_incorrect_blog_list(self):
        url = '/api/blog/.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # GET /api/blog/1.json
    def test_json_blogentry(self):
        url = '/api/blog/1.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # GET /blog1.json
    def test_json_inccorect_blogentry(self):
        url = '/api/blog1.json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
