from django.urls import reverse
from django.test import Client, TestCase

from blog.models import BlogEntry


class BlogEntryViewLoggedInTests(TestCase):
    """User testing the views is logged in and has all required permissions."""
    fixtures = ['blog_views_testdata', 'users_views_testdata']
    csrf_client = Client(enforce_csrf_checks=True)

    def setUp(self):
        self.client.login(username='john.doe', password='john.doe')

    # List
    def test_get_list_view(self):
        response = self.client.get(reverse('blog:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('blog', response.context)
        self.assertEqual(list(response.context['blog']), list(BlogEntry.objects.all()))

    def test_post_list_view_not_allowed(self):
        response = self.client.post(reverse('blog:list'))
        self.assertEqual(response.status_code, 405)

    # Detail
    def test_get_detail_view(self):
        response = self.client.get(reverse('blog:detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('blogentry', response.context)
        self.assertEqual(response.context['blogentry'], BlogEntry.objects.get(pk=1))

    def test_get_detail_view_not_existant(self):
        response = self.client.get(reverse('blog:detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_view_not_allowed(self):
        response = self.client.post(reverse('blog:detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 405)

    # Create
    def test_get_create_view(self):
        response = self.client.get(reverse('blog:create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_post_create_view(self):
        data = {
            'title': 'Random BlogEntry',
            'content': '<p> blog entry </p>',
            'status': BlogEntry.DRAFT,
        }
        response = self.client.post(reverse('blog:create'), data, follow=True)
        self.assertRedirects(response, reverse('blog:detail', kwargs={'pk': BlogEntry.objects.count()}))

    def test_post_create_view_no_data(self):
        response = self.client.post(reverse('blog:create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_create_view_incomplete_data(self):
        data = {
            'title': 'Random BlogEntry',
        }
        response = self.client.post(reverse('blog:create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_create_view_without_csrf_token(self):
        response = self.csrf_client.post(reverse('blog:create'))
        self.assertEqual(response.status_code, 403)

    # Update
    def test_get_update_view(self):
        response = self.client.get(reverse('blog:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_get_update_view_not_existant(self):
        response = self.client.get(reverse('blog:update', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_update_view(self):
        data = {
            'title': 'Random BlogEntry',
            'content': '<p> blog entry </p>',
            'status': BlogEntry.DRAFT,
        }
        response = self.client.post(reverse('blog:update', kwargs={'pk': 1}), data, follow=True)
        self.assertRedirects(response, reverse('blog:detail', kwargs={'pk': 1}))

    def test_post_update_view_no_data(self):
        response = self.client.post(reverse('blog:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_update_view_incomplete_data(self):
        data = {
            'name': 'Updated BlogEntry',
        }
        response = self.client.post(reverse('blog:update', kwargs={'pk': 1}), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_update_view_not_existant(self):
        response = self.client.post(reverse('blog:update', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_update_view_without_csrf_token(self):
        response = self.csrf_client.post(reverse('blog:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)

    # Delete
    def test_get_delete_view(self):
        response = self.client.get(reverse('blog:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('blogentry', response.context)
        self.assertEqual(response.context['blogentry'], BlogEntry.objects.get(pk=1))

    def test_get_delete_view_not_existant(self):
        response = self.client.get(reverse('blog:delete', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_delete_view(self):
        response = self.client.post(reverse('blog:delete', kwargs={'pk': 1}), follow=True)
        self.assertRedirects(response, reverse('blog:list'))
        self.assertIsNone(BlogEntry.objects.filter(pk=1).first())

    def test_post_delete_view_not_existant(self):
        response = self.client.post(reverse('blog:delete', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_post_delete_view_without_csrf_token(self):
        response = self.csrf_client.post(reverse('blog:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)


class BlogEntryViewNoPermissionTests(TestCase):
    """User testing the views is not logged and therefore lacking the required permissions."""
    # List
    def test_get_list_view(self):
        url = reverse('blog:list')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Detail
    def test_get_detail_view(self):
        url = reverse('blog:detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Create
    def test_get_create_view(self):
        url = reverse('blog:create')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Update
    def test_get_update_view(self):
        url = reverse('blog:update', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    # Delete
    def test_get_delete_view(self):
        url = reverse('blog:delete', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)
