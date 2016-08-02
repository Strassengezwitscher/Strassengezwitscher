from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth

from strassengezwitscher.models import MapObject


class StrassengezwitscherTests(TestCase):
    def test_serves_angular_tag(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<sg-app>', response.content)
        self.assertIn(b'</sg-app>', response.content)

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


class MapObjectModelTests(TestCase):
    def test_representation(self):
        obj = MapObject(name='Test')
        self.assertEqual(repr(obj), '<MapObject Test>')

    def test_string_representation(self):
        obj = MapObject(name='Test')
        self.assertEqual(str(obj), 'Test')
