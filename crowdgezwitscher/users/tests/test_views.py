from django.urls import reverse
from django.test import Client, TestCase

from django.contrib.auth import get_user
from django.contrib.auth.models import User, Group


class UserViewLoggedInTests(TestCase):
    """User testing the views is logged in and has all required permissions."""
    fixtures = ['users_views_testdata']
    csrf_client = Client(enforce_csrf_checks=True)

    def setUp(self):
        self.client.login(username='adm', password='adm')

    # List
    def test_get_list_view(self):
        response = self.client.get(reverse('users:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('users', response.context)
        self.assertEqual(len(response.context['users']), 3)  # Don't show superusers

    def test_post_list_view_not_allowed(self):
        response = self.client.post(reverse('users:list'))
        self.assertEqual(response.status_code, 405)

    # Detail
    def test_get_detail_view(self):
        response = self.client.get(reverse('users:detail', kwargs={'pk': 3}))  # todo
        self.assertEqual(response.status_code, 200)
        self.assertIn('user_data', response.context)
        self.assertEqual(response.context['user_data'], User.objects.get(pk=3))

    def test_get_detail_view_not_existant(self):
        response = self.client.get(reverse('users:detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_view_not_allowed(self):
        response = self.client.post(reverse('users:detail', kwargs={'pk': 3}))
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
        self.assertRedirects(response, reverse('users:detail', kwargs={'pk': 5}))
        self.assertNotEqual(User.objects.get(pk=5).password, '123456', 'User password is stored as hash.')

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
        response = self.client.get(reverse('users:update', kwargs={'pk': 3}))
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
        response = self.client.post(reverse('users:update', kwargs={'pk': 3}), data, follow=True)
        self.assertRedirects(response, reverse('users:detail', kwargs={'pk': 3}))
        self.assertNotEqual(User.objects.get(pk=3).password, '123456', 'User password is stored as hash.')

    def test_post_update_view_no_data(self):
        response = self.client.post(reverse('users:update', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_update_view_incomplete_data(self):
        data = {
            'name': 'Updated User',
        }
        response = self.client.post(reverse('users:update', kwargs={'pk': 3}), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_update_view_not_existant(self):
        response = self.client.post(reverse('users:update', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_update_view_without_csrf_token(self):
        response = self.csrf_client.post(reverse('users:update', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 403)


class UserViewLoggedOutTests(TestCase):
    """User testing the views is not logged."""
    # List
    def test_get_list_view(self):
        url = reverse('users:list')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Detail
    def test_get_detail_view(self):
        url = reverse('users:detail', kwargs={'pk': 3})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Create
    def test_get_create_view(self):
        url = reverse('users:create')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Update
    def test_get_update_view(self):
        url = reverse('users:update', kwargs={'pk': 3})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)


class UserViewNoPermissionTests(TestCase):
    """User testing the views is logged in as a Moderator but lacks the required permissons."""
    fixtures = ['users_views_testdata']

    def setUp(self):
        self.client.login(username='john.doe', password='john.doe')

    def test_logged_in_as_moderator(self):
        user = get_user(self.client)
        mod_group = Group.objects.get(name='Moderatoren')
        self.assertEqual(list(user.groups.all()), [mod_group])
    
    # List
    def test_get_list_view(self):
        url = reverse('users:list')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Detail
    def test_get_detail_view(self):
        url = reverse('users:detail', kwargs={'pk': 3})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Create
    def test_get_create_view(self):
        url = reverse('users:create')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Update
    def test_get_update_view(self):
        url = reverse('users:update', kwargs={'pk': 3})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)
