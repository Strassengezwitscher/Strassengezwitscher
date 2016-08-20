from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client, TestCase

from events.models import Event


class EventViewLoggedInTests(TestCase):
    """User testing the views is logged in and has all required permissions."""
    fixtures = ['events_views_testdata', 'users_views_testdata']
    csrf_client = Client(enforce_csrf_checks=True)

    def setUp(self):
        self.client.login(username='john.doe', password='john.doe')

    # List
    def test_get_list_view(self):
        response = self.client.get(reverse('events:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('events', response.context)
        self.assertEqual(list(response.context['events']), list(Event.objects.all()))

    def test_post_list_view_not_allowed(self):
        response = self.client.post(reverse('events:list'))
        self.assertEqual(response.status_code, 405)

    # Detail
    def test_get_detail_view(self):
        response = self.client.get(reverse('events:detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('event', response.context)
        self.assertEqual(response.context['event'], Event.objects.get(pk=1))

    def test_get_detail_view_not_existant(self):
        response = self.client.get(reverse('events:detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_view_not_allowed(self):
        response = self.client.post(reverse('events:detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 405)

    # Create
    def test_get_create_view(self):
        response = self.client.get(reverse('events:create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_post_create_view(self):
        data = {
            'name': 'Random Event',
            'active': True,
            'location_lat': 0.0,
            'location_long': 0.0,
            'date': '2013-05-16',
            'repetition_cycle': 'unbekannter Rhythmus',
            'organizer': 'you',
            'type': 'classic event',
            'url': 'http://google.com',
            'counter_event': False,
            'coverage': False,
        }
        response = self.client.post(reverse('events:create'), data, follow=True)
        self.assertRedirects(response, reverse('events:detail', kwargs={'pk': 4}))

    def test_post_create_view_no_data(self):
        response = self.client.post(reverse('events:create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_create_view_incomplete_data(self):
        data = {
            'name': 'Random Event',
        }
        response = self.client.post(reverse('events:create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_create_view_without_csrf_token(self):
        response = self.csrf_client.post(reverse('events:create'))
        self.assertEqual(response.status_code, 403)

    # Update
    def test_get_update_view(self):
        response = self.client.get(reverse('events:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_get_update_view_not_existant(self):
        response = self.client.get(reverse('events:update', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_update_view(self):
        data = {
            'name': 'Updated Event',
            'active': True,
            'location_lat': 0.0,
            'location_long': 0.0,
            'date': '2013-05-16',
            'repetition_cycle': 'unbekannter Rhythmus',
            'organizer': 'you',
            'type': 'classic event',
            'url': 'http://google.com',
            'counter_event': False,
            'coverage': False,
        }
        response = self.client.post(reverse('events:update', kwargs={'pk': 1}), data, follow=True)
        self.assertRedirects(response, reverse('events:detail', kwargs={'pk': 1}))

    def test_post_update_view_no_data(self):
        response = self.client.post(reverse('events:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_update_view_incomplete_data(self):
        data = {
            'name': 'Updated Event',
        }
        response = self.client.post(reverse('events:update', kwargs={'pk': 1}), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_update_view_not_existant(self):
        response = self.client.post(reverse('events:update', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_update_view_without_csrf_token(self):
        response = self.csrf_client.post(reverse('events:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)

    # Delete
    def test_get_delete_view(self):
        response = self.client.get(reverse('events:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('event', response.context)
        self.assertEqual(response.context['event'], Event.objects.get(pk=1))

    def test_get_delete_view_not_existant(self):
        response = self.client.get(reverse('events:delete', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_delete_view(self):
        response = self.client.post(reverse('events:delete', kwargs={'pk': 1}), follow=True)
        self.assertRedirects(response, reverse('events:list'))
        self.assertIsNone(Event.objects.filter(pk=1).first())

    def test_post_delete_view_not_existant(self):
        response = self.client.post(reverse('events:delete', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_delete_view_without_csrf_token(self):
        response = self.csrf_client.post(reverse('events:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)


class EventViewNoPermissionTests(TestCase):
    """User testing the views is not logged and therefore lacking the required permissions."""
    # List
    def test_get_list_view(self):
        url = reverse('events:list')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Detail
    def test_get_detail_view(self):
        url = reverse('events:detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Create
    def test_get_create_view(self):
        url = reverse('events:create')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Update
    def test_get_update_view(self):
        url = reverse('events:update', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Delete
    def test_get_delete_view(self):
        url = reverse('events:delete', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)
