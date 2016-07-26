from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from django.contrib.auth.models import User


class UserViewTests(TestCase):
    fixtures = ['users_views_testdata']
    csrf_client = Client(enforce_csrf_checks=True)

    # List
    def test_get_list_view(self):
        response = self.client.get(reverse('users:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('users', response.context)
        self.assertEqual(list(response.context['users']), list(User.objects.all()))

    def test_post_list_view_not_allowed(self):
        response = self.client.post(reverse('users:list'))
        self.assertEqual(response.status_code, 405)

    # Detail
    def test_get_detail_view(self):
        response = self.client.get(reverse('users:detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], User.objects.get(pk=1))

    def test_get_detail_view_not_existant(self):
        response = self.client.get(reverse('users:detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_view_not_allowed(self):
        response = self.client.post(reverse('users:detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 405)

    # Create
    def test_get_create_view(self):
        response = self.client.get(reverse('users:create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_post_create_view(self):
        data = {
            'username': 'Random.User',
            'email': 'random@user.com',
            'password': '123456',
        }
        response = self.client.post(reverse('users:create'), data, follow=True)
        self.assertRedirects(response, reverse('users:detail', kwargs={'pk': 3}))

    def test_post_create_view_no_data(self):
        response = self.client.post(reverse('users:create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_create_view_incomplete_data(self):
        data = {
            'username': 'Random User',
        }
        response = self.client.post(reverse('users:create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_create_view_without_csrf_token(self):
        response = self.csrf_client.post(reverse('users:create'))
        self.assertEqual(response.status_code, 403)

    # Update
    def test_get_update_view(self):
        response = self.client.get(reverse('users:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_get_update_view_not_existant(self):
        response = self.client.get(reverse('users:update', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_update_view(self):
        data = {
            'username': 'Random.User',
            'email': 'random@user.com',
            'password': '123456',
        }
        response = self.client.post(reverse('users:update', kwargs={'pk': 1}), data, follow=True)
        self.assertRedirects(response, reverse('users:detail', kwargs={'pk': 1}))

    def test_post_update_view_no_data(self):
        response = self.client.post(reverse('users:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_update_view_incomplete_data(self):
        data = {
            'name': 'Updated User',
        }
        response = self.client.post(reverse('users:update', kwargs={'pk': 1}), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_update_view_not_existant(self):
        response = self.client.post(reverse('users:update', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_update_view_without_csrf_token(self):
        response = self.csrf_client.post(reverse('users:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)
