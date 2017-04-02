from django.urls import reverse
from django.test import Client, TestCase
import mock
from TwitterAPI import TwitterResponse

from twitter.models import TwitterAccount


class TwitterAccountViewCorrectPermissionMixin(object):
    """User testing the views is logged in and has all required permissions."""
    csrf_client = Client(enforce_csrf_checks=True)

    # List
    def test_get_list_view(self):
        response = self.client.get(reverse('twitter:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('accounts', response.context)
        self.assertEqual(list(response.context['accounts']), list(TwitterAccount.objects.all()))

    def test_post_list_view_not_allowed(self):
        response = self.client.post(reverse('twitter:list'))
        self.assertEqual(response.status_code, 405)

    # Detail
    def test_get_detail_view(self):
        response = self.client.get(reverse('twitter:detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('account', response.context)
        self.assertEqual(response.context['account'], TwitterAccount.objects.get(pk=1))

    def test_get_detail_view_not_existant(self):
        response = self.client.get(reverse('twitter:detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_view_not_allowed(self):
        response = self.client.post(reverse('twitter:detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 405)

    # Create
    def test_get_create_view(self):
        response = self.client.get(reverse('twitter:create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def mocked_requests_get(*args):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        if args[1] == 'users/show':
            r = MockResponse({"id_str": "1337"}, 200)
            return TwitterResponse(r, None)

    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('TwitterAPI.TwitterAPI.request', mocked_requests_get)
    def test_post_create_view(self):
        data = {
            'name': 'Random Account',
        }
        response = self.client.post(reverse('twitter:create'), data, follow=True)
        self.assertRedirects(response, reverse('twitter:detail', kwargs={'pk': 2}))

    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('TwitterAPI.TwitterAPI.request', mocked_requests_get)
    def test_post_create_view_no_data(self):
        response = self.client.post(reverse('twitter:create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    @mock.patch('TwitterAPI.TwitterAPI.__init__', mock.Mock(return_value=None))
    @mock.patch('TwitterAPI.TwitterAPI.request', mocked_requests_get)
    def test_post_create_view_incomplete_data(self):
        data = {}
        response = self.client.post(reverse('twitter:create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_create_view_without_csrf_token(self):
        response = self.csrf_client.post(reverse('twitter:create'))
        self.assertEqual(response.status_code, 403)

    # Delete
    def test_get_delete_view(self):
        response = self.client.get(reverse('twitter:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('account', response.context)
        self.assertEqual(response.context['account'], TwitterAccount.objects.get(pk=1))

    def test_get_delete_view_not_existant(self):
        response = self.client.get(reverse('twitter:delete', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_delete_view(self):
        response = self.client.post(reverse('twitter:delete', kwargs={'pk': 1}), follow=True)
        self.assertRedirects(response, reverse('twitter:list'))
        self.assertIsNone(TwitterAccount.objects.filter(pk=1).first())

    def test_post_delete_view_not_existant(self):
        response = self.client.post(reverse('twitter:delete', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_delete_view_without_csrf_token(self):
        response = self.csrf_client.post(reverse('twitter:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)


class TwitterAccountViewWrongPermissionMixin(object):
    """User testing the views is not logged and therefore lacking the required permissions."""
    # List
    def test_get_list_view(self):
        url = reverse('twitter:list')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Detail
    def test_get_detail_view(self):
        url = reverse('twitter:detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Create
    def test_get_create_view(self):
        url = reverse('twitter:create')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Delete
    def test_get_delete_view(self):
        url = reverse('twitter:delete', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)


class TwitterAccountViewAdministratorTests(TestCase, TwitterAccountViewCorrectPermissionMixin):
    """User testing the views is logged in as Administrator"""
    fixtures = ['twitter_views_testdata', 'users_views_testdata']

    def setUp(self):
        self.client.login(username='adm', password='adm')


class TwitterAccountViewModeratorTests(TestCase, TwitterAccountViewCorrectPermissionMixin):
    """User testing the views is logged in as Moderator"""
    fixtures = ['twitter_views_testdata', 'users_views_testdata']

    def setUp(self):
        self.client.login(username='john.doe', password='john.doe')


class TwitterAccountViewNoPermissionTests(TestCase, TwitterAccountViewWrongPermissionMixin):
    """User testing the views is not logged in"""
    fixtures = ['twitter_views_testdata', 'users_views_testdata']
