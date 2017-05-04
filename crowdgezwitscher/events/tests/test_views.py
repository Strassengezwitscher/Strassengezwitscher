# -*- coding: utf-8 -*-
import os
import tempfile
from unittest import mock

from django.urls import reverse
from django.test import Client, TestCase
from django.utils.timezone import now

from events.models import Event, Attachment


class EventTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super(EventTestCase, self).__init__(*args, **kwargs)
        self.empty_formset = {
            'attachments-TOTAL_FORMS': 0,
            'attachments-INITIAL_FORMS': 0,
        }
        self.post_data = self.empty_formset.copy()
        self.post_data.update({
            'name': 'Random Event',
            'active': True,
            'location_lat': 0.1234567,
            'location_long': 0.1234567,
            'location': 'Water',
            'date': '2013-05-16',
            'repetition_cycle': 'unbekannter Rhythmus',
            'organizer': 'you',
            'type': 'classic event',
            'url': 'http://google.com',
            'counter_event': False,
            'coverage': False,
        })

    def tearDown(self):
        Attachment.objects.all().delete()  # not only delete DB entries but also the actual files from disk


class EventViewCorrectPermissionMixin(object):
    """User testing the views is logged in and has all required permissions."""
    csrf_client = Client(enforce_csrf_checks=True)

    # List
    def test_get_list_view(self):
        response = self.client.get(reverse('events:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('events', response.context)
        events = list(response.context['events'])
        all_events = Event.objects.all()
        self.assertTrue(all([event in all_events for event in events]))
        # Events are sorted by date in descending order
        self.assertEqual(events, sorted(all_events, key=lambda event: event.date, reverse=True))

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

    def test_post_create_view_without_attachments(self):
        response = self.client.post(reverse('events:create'), self.post_data, follow=True)
        self.assertRedirects(response, reverse('events:detail', kwargs={'pk': 4}))
        self.assertEqual(Attachment.objects.count(), 3)

    @mock.patch('random.choice', lambda *args, **kwargs: 'x')
    def test_post_create_view_with_one_attachment(self):
        attachment_name = "dolphin      diary.TXT"
        attachment_content = "Thanks for all the fish."
        attachment_description = "A diary written by dolphins."
        tempdir = tempfile.gettempdir()
        f = open(os.path.join(tempdir, attachment_name), 'w+')
        f.write(attachment_content)
        f.seek(0)
        self.post_data.update({
            'attachments-TOTAL_FORMS': 1,
            'attachments-0-attachment': f,
            'attachments-0-description': attachment_description,
            'attachments-0-public': True,
        })
        response = self.client.post(reverse('events:create'), self.post_data, follow=True)
        self.assertRedirects(response, reverse('events:detail', kwargs={'pk': 4}))
        self.assertEqual(Attachment.objects.count(), 4)
        attachment = Attachment.objects.get(pk=4)
        self.assertEqual(attachment.name, attachment_name)
        self.assertEqual(attachment.description, attachment_description)
        self.assertEqual(attachment.public, True)
        self.assertEqual(attachment.event.id, 4)
        self.assertEqual(str(attachment.attachment),
                         'event_attachments/%s_dolphindiary_xxxxx.txt' % now().strftime("%Y/%m/%Y%m%d-%H%M"))

    @mock.patch('random.choice', lambda *args, **kwargs: 'x')
    def test_post_create_view_with_multiple_attachments(self):
        attachment_name = "dolphin      diary.TXT"
        attachment_content = "Thanks for all the fish."
        attachment_description = "A diary written by dolphins."
        tempdir = tempfile.gettempdir()
        file1 = open(os.path.join(tempdir, attachment_name), 'w+')
        file1.write(attachment_content)
        file1.seek(0)
        file2 = open(os.path.join(tempdir, attachment_name + '2'), 'w+')
        file2.write(attachment_content)
        file2.seek(0)
        self.post_data.update({
            'attachments-TOTAL_FORMS': 2,
            'attachments-0-attachment': file1,
            'attachments-0-description': attachment_description,
            'attachments-0-public': False,
            'attachments-1-attachment': file2,
            'attachments-1-description': attachment_description + '2',
            'attachments-1-public': False,
        })
        response = self.client.post(reverse('events:create'), self.post_data, follow=True)
        self.assertRedirects(response, reverse('events:detail', kwargs={'pk': 4}))
        self.assertEqual(Attachment.objects.count(), 5)
        attachment1 = Attachment.objects.get(pk=4)
        self.assertEqual(attachment1.name, attachment_name)
        self.assertEqual(attachment1.description, attachment_description)
        self.assertEqual(attachment1.public, False)
        self.assertEqual(attachment1.event.id, 4)
        self.assertEqual(str(attachment1.attachment),
                         'event_attachments/%s_dolphindiary_xxxxx.txt' % now().strftime("%Y/%m/%Y%m%d-%H%M"))
        attachment2 = Attachment.objects.get(pk=5)
        self.assertEqual(attachment2.name, attachment_name + '2')
        self.assertEqual(attachment2.description, attachment_description + '2')
        self.assertEqual(attachment2.public, False)
        self.assertEqual(attachment2.event.id, 4)
        self.assertEqual(str(attachment2.attachment),
                         'event_attachments/%s_dolphindiary_xxxxx.txt2' % now().strftime("%Y/%m/%Y%m%d-%H%M"))

    def test_post_create_view_coverage_valid_1(self):
        post_data = self.post_data.copy()
        post_data.update({
            'coverage': True,
            'twitter_account_names': 'Foobar',
            'coverage_start': '2017-01-01',
            'coverage_end': '2017-01-02',
        })
        response = self.client.post(reverse('events:create'), post_data, follow=True)
        self.assertRedirects(response, reverse('events:detail', kwargs={'pk': 4}))

    def test_post_create_view_coverage_valid_2(self):
        post_data = self.post_data.copy()
        post_data.update({
            'coverage': False,
            'coverage_start': '2017-01-01',
            'coverage_end': '2017-01-02',
        })
        response = self.client.post(reverse('events:create'), post_data, follow=True)
        self.assertRedirects(response, reverse('events:detail', kwargs={'pk': 4}))

    def test_post_create_view_coverage_valid_3(self):
        post_data = self.post_data.copy()
        post_data.update({
            'coverage': False,
            'coverage_start': '2017-01-01',
            'coverage_end': '2017-01-01',
        })
        response = self.client.post(reverse('events:create'), post_data, follow=True)
        self.assertRedirects(response, reverse('events:detail', kwargs={'pk': 4}))

    def test_post_create_view_coverage_valid_4(self):
        post_data = self.post_data.copy()
        post_data.update({
            'coverage': False,
            'coverage_start': '',
            'coverage_end': '',
        })
        response = self.client.post(reverse('events:create'), post_data, follow=True)
        self.assertRedirects(response, reverse('events:detail', kwargs={'pk': 4}))

    def test_post_create_view_coverage_valid_5(self):
        post_data = self.post_data.copy()
        post_data.update({
            'coverage': False,
            'coverage_start': '2017-01-01',
            'coverage_end': '',
        })
        response = self.client.post(reverse('events:create'), post_data, follow=True)
        self.assertRedirects(response, reverse('events:detail', kwargs={'pk': 4}))

    def test_post_create_view_coverage_missing_2(self):
        post_data = self.post_data.copy()
        post_data.update({
            'coverage': False,
            'coverage_start': '',
            'coverage_end': '2017-01-02',
        })
        response = self.client.post(reverse('events:create'), post_data, follow=True)
        self.assertRedirects(response, reverse('events:detail', kwargs={'pk': 4}))

    def test_post_create_view_coverage_invalid_dates(self):
        post_data = self.post_data.copy()
        post_data.update({
            'coverage': False,
            'coverage_start': '2017-01-02',
            'coverage_end': '2017-01-01',
        })
        response = self.client.post(reverse('events:create'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again
        self.assertFormError(response, 'form', 'coverage_start', "'coverage_start' muss vor 'coverage_end' liegen")
        self.assertFormError(response, 'form', 'coverage_end', "'coverage_start' muss vor 'coverage_end' liegen")

    def test_post_create_view_coverage_invalid_fields_missing(self):
        post_data = self.post_data.copy()
        post_data.update({
            'coverage': True,
        })
        response = self.client.post(reverse('events:create'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again
        self.assertFormError(response, 'form', 'coverage', "Nicht alle benötigen Felder wurden ausgefüllt")
        self.assertFormError(response, 'form', 'twitter_account_names', "Wird für eine Berichterstattung benötigt")
        self.assertFormError(response, 'form', 'coverage_start', "Wird für eine Berichterstattung benötigt")
        self.assertFormError(response, 'form', 'coverage_end', "Wird für eine Berichterstattung benötigt")

    def test_post_create_view_no_data(self):
        response = self.client.post(reverse('events:create'), self.empty_formset)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_create_view_incomplete_data(self):
        data = {
            'name': 'Random Event',
        }
        data.update(self.empty_formset)
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

    def test_post_update_view_with_unchanged_attachments(self):
        self.assertEqual(Attachment.objects.count(), 3)
        self.post_data.update({'name': 'Updated Event'})
        response = self.client.post(reverse('events:update', kwargs={'pk': 1}), self.post_data, follow=True)
        self.assertEqual(Event.objects.get(pk=1).name, 'Updated Event')
        self.assertRedirects(response, reverse('events:detail', kwargs={'pk': 1}))
        self.assertEqual(Attachment.objects.count(), 3)

    def test_post_update_view_with_deleted_attachment(self):
        self.assertEqual(Attachment.objects.count(), 3)
        self.post_data.update({
            'attachments-TOTAL_FORMS': 4,
            'attachments-INITIAL_FORMS': 3,
            'attachments-0-id': 1,
            'attachments-0-DELETE': 'on',
            'attachments-1-id': 2,
            'attachments-1-DELETE': 'on',
            'attachments-2-id': 3,
            'attachments-2-DELETE': 'on',
        })
        response = self.client.post(reverse('events:update', kwargs={'pk': 1}), self.post_data, follow=True)
        self.assertRedirects(response, reverse('events:detail', kwargs={'pk': 1}))
        self.assertEqual(Attachment.objects.count(), 0)

    def test_post_update_view_no_data(self):
        response = self.client.post(reverse('events:update', kwargs={'pk': 1}), self.empty_formset)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)  # shows form again

    def test_post_update_view_incomplete_data(self):
        data = {
            'name': 'Updated Event',
        }
        data.update(self.empty_formset)
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


class EventViewWrongPermissionMixin(object):
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


class EventViewAdministratorTests(EventTestCase, EventViewCorrectPermissionMixin):
    """User testing the views is logged in as Administrator"""
    fixtures = ['events_views_testdata', 'users_views_testdata']

    def setUp(self):
        self.client.login(username='adm', password='adm')


class EventViewModeratorTests(EventTestCase, EventViewCorrectPermissionMixin):
    """User testing the views is logged in as Moderator"""
    fixtures = ['events_views_testdata', 'users_views_testdata']

    def setUp(self):
        self.client.login(username='john.doe', password='john.doe')


class EventViewNoPermissionTests(EventTestCase, EventViewWrongPermissionMixin):
    """User testing the views is not logged in"""
    fixtures = ['events_views_testdata', 'users_views_testdata']
