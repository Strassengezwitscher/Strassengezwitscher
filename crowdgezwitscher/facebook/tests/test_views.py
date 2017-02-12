from django.urls import reverse
from django.test import Client, TestCase

from facebook.models import FacebookPage


class FacebookPageViewCorrectPermissionMixin(object):
    """User testing the views is logged in and has all required permissions."""
    csrf_client = Client(enforce_csrf_checks=True)

    # List
    def test_get_list_view(self):
        response = self.client.get(reverse('facebook:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('pages', response.context)
        self.assertEqual(list(response.context['pages']), list(FacebookPage.objects.all()))

    def test_post_list_view_not_allowed(self):
        response = self.client.post(reverse('facebook:list'))
        self.assertEqual(response.status_code, 405)

    # Detail
    def test_get_detail_view(self):
        response = self.client.get(reverse('facebook:detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('page', response.context)
        self.assertEqual(response.context['page'], FacebookPage.objects.get(pk=1))

    def test_get_detail_view_not_existant(self):
        response = self.client.get(reverse('facebook:detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_view_not_allowed(self):
        response = self.client.post(reverse('facebook:detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 405)

    # Create
    def test_get_create_view(self):
        response = self.client.get(reverse('facebook:create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_post_create_view(self):
        data = {
            'name': 'Random Facebook Page',
            'active': True,
            'location_lat': 0.1234567,
            'location_long': 0.1234567,
            'location': 'Water',
            'notes': 'Random Note',
            'facebook_id': '1234567890',
        }
        response = self.client.post(reverse('facebook:create'), data, follow=True)
        self.assertRedirects(response, reverse('facebook:detail', kwargs={'pk': 4}))

    def test_post_create_view_no_data(self):
        response = self.client.post(reverse('facebook:create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_create_view_incomplete_data(self):
        data = {
            'name': 'Random Facebook Page',
        }
        response = self.client.post(reverse('facebook:create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_create_view_without_csrf_token(self):
        response = self.csrf_client.post(reverse('facebook:create'))
        self.assertEqual(response.status_code, 403)

    # Update
    def test_get_update_view(self):
        response = self.client.get(reverse('facebook:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_get_update_view_not_existant(self):
        response = self.client.get(reverse('facebook:update', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_update_view(self):
        data = {
            'name': 'Updated Facebook Page',
            'active': True,
            'location_lat': 0.1234567,
            'location_long': 0.1234567,
            'location': 'Water',
            'notes': 'Random Note',
            'facebook_id': '1234567890',
        }
        response = self.client.post(reverse('facebook:update', kwargs={'pk': 1}), data, follow=True)
        self.assertRedirects(response, reverse('facebook:detail', kwargs={'pk': 1}))

    def test_post_update_view_no_data(self):
        response = self.client.post(reverse('facebook:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_update_view_incomplete_data(self):
        data = {
            'name': 'Updated Facebook Page',
        }
        response = self.client.post(reverse('facebook:update', kwargs={'pk': 1}), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_update_view_not_existant(self):
        response = self.client.post(reverse('facebook:update', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_update_view_without_csrf_token(self):
        response = self.csrf_client.post(reverse('facebook:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)

    # Delete
    def test_get_delete_view(self):
        response = self.client.get(reverse('facebook:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('page', response.context)
        self.assertEqual(response.context['page'], FacebookPage.objects.get(pk=1))

    def test_get_delete_view_not_existant(self):
        response = self.client.get(reverse('facebook:delete', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_delete_view(self):
        response = self.client.post(reverse('facebook:delete', kwargs={'pk': 1}), follow=True)
        self.assertRedirects(response, reverse('facebook:list'))
        self.assertIsNone(FacebookPage.objects.filter(pk=1).first())

    def test_post_delete_view_not_existant(self):
        response = self.client.post(reverse('facebook:delete', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_delete_view_without_csrf_token(self):
        response = self.csrf_client.post(reverse('facebook:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)


class FacebookPageViewWrongPermissionMixin(object):
    """User testing the views is not logged and therefore lacking the required permissions."""
    # List
    def test_get_list_view(self):
        url = reverse('facebook:list')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Detail
    def test_get_detail_view(self):
        url = reverse('facebook:detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Create
    def test_get_create_view(self):
        url = reverse('facebook:create')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Update
    def test_get_update_view(self):
        url = reverse('facebook:update', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Delete
    def test_get_delete_view(self):
        url = reverse('facebook:delete', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)


class FacebookPageViewAdministratorTests(TestCase, FacebookPageViewCorrectPermissionMixin):
    """User testing the views is logged in as Administrator"""
    fixtures = ['facebook_views_testdata', 'users_views_testdata']

    def setUp(self):
        self.client.login(username='adm', password='adm')


class FacebookPageViewModeratorTests(TestCase, FacebookPageViewCorrectPermissionMixin):
    """User testing the views is logged in as Moderator"""
    fixtures = ['facebook_views_testdata', 'users_views_testdata']

    def setUp(self):
        self.client.login(username='john.doe', password='john.doe')


class FacebookPageViewNoPermissionTests(TestCase, FacebookPageViewWrongPermissionMixin):
    """User testing the views is not logged in"""
    fixtures = ['facebook_views_testdata', 'users_views_testdata']
