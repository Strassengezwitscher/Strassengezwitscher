from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth


class CrowdgezwitscherViewTests(TestCase):
    def test_serves_angular_tag(self):
        url_names = ['map', 'contact', 'imprint', 'about', 'support', 'eventDetail', 'blog']
        for url_name in url_names:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<cg-app>', response.content)
            self.assertIn(b'</cg-app>', response.content)

    def login(self):
        self.user = User.objects.create_user('user', 'user@host.org', 'password')
        data = {
            'username': 'user',
            'password': 'password'
        }
        return self.client.post(reverse('login'), data, follow=True)

    def test_login(self):
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())
        response = self.login()
        self.assertRedirects(response, reverse('intern'))
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())

    def test_logout(self):
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())
        self.login()
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())

    def test_intern_logged_in(self):
        self.user = User.objects.create_user('user', 'user@host.org', 'password')
        self.client.login(username='user', password='password')
        url = reverse('intern')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_intern_logged_out(self):
        url = reverse('intern')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_mattermost_url_logged_in(self):
        self.user = User.objects.create_user('user', 'user@host.org', 'password')
        self.client.login(username='user', password='password')
        url = reverse('mattermost')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_mattermost_url_logged_out(self):
        url = reverse('mattermost')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_landingpage_url(self):
        response = self.client.get(reverse('landingpage'))
        self.assertEqual(response.status_code, 200)

    def test_change_password_get_form(self):
        self.user = User.objects.create_user('user', 'user@host.org', 'password')
        self.client.login(username='user', password='password')
        url = reverse('change_password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_change_password(self):
        self.user = User.objects.create_user('user', 'user@host.org', 'password')
        self.client.login(username='user', password='password')
        data = {
            'old_password': 'password',
            'new_password1': 'password-new',
            'new_password2': 'password-new',
        }
        response = self.client.post(reverse('change_password'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].success)

    def test_change_password_old_password_not_matching(self):
        self.user = User.objects.create_user('user', 'user@host.org', 'password')
        self.client.login(username='user', password='password')
        url = reverse('change_password')
        data = {
            'old_password': 'password-wrong',
            'new_password1': 'password-new',
            'new_password2': 'password-new',
        }
        response = self.client.post(reverse('change_password'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].success)
        self.assertIn('old_password', response.context['form'].errors)

    def test_change_password_new_passwords_not_matching(self):
        self.user = User.objects.create_user('user', 'user@host.org', 'password')
        self.client.login(username='user', password='password')
        data = {
            'old_password': 'password',
            'new_password1': 'password-new',
            'new_password2': 'password-new-wrong',
        }
        response = self.client.post(reverse('change_password'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].success)
        self.assertIn('new_password2', response.context['form'].errors)
