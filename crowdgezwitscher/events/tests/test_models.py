from datetime import date
import os
import tempfile
from unittest import mock

from PIL import Image

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.timezone import now

from events.models import Event, Attachment


class EventModelTests(TestCase):
    def test_representation(self):
        event = Event(name='Test', date=date(2012, 12, 21), organizer="Organizer")
        self.assertEqual(repr(event), '<Event Test at 2012-12-21 by Organizer>')

    def test_representation_date_only(self):
        event = Event(date=date(2012, 12, 21))
        self.assertEqual(repr(event), '<Event unbenannt at 2012-12-21>')

    def test_representation_date_and_name(self):
        event = Event(name='Test', date=date(2012, 12, 21))
        self.assertEqual(repr(event), '<Event Test at 2012-12-21>')

    def test_representation_date_and_organizer(self):
        event = Event(date=date(2012, 12, 21), organizer="Organizer")
        self.assertEqual(repr(event), '<Event unbenannt at 2012-12-21 by Organizer>')

    def test_string_representation(self):
        event = Event(name='Test', date=date(2012, 12, 21), organizer="Organizer")
        self.assertEqual(str(event), 'Test at 2012-12-21 by Organizer')

    def test_string_representation_date_only(self):
        event = Event(date=date(2012, 12, 21))
        self.assertEqual(str(event), 'unbenannt at 2012-12-21')

    def test_string_representation_date_and_name(self):
        event = Event(name='Test', date=date(2012, 12, 21))
        self.assertEqual(str(event), 'Test at 2012-12-21')

    def test_string_representation_date_and_organizer(self):
        event = Event(date=date(2012, 12, 21), organizer="Organizer")
        self.assertEqual(str(event), 'unbenannt at 2012-12-21 by Organizer')

    def test__is_ready_for_twitter(self):
        event = Event(twitter_account_names='foo,bar', coverage_start=date(2016, 9, 27))
        self.assertFalse(event._is_ready_for_twitter())
        event.coverage_end = date(2016, 9, 28)
        self.assertTrue(event._is_ready_for_twitter())

    def test_build_twitter_search_query(self):
        event = Event(twitter_hashtags='baz', coverage_start=date(2016, 9, 27), coverage_end=date(2016, 9, 28))
        self.assertIsNone(event.build_twitter_search_query())
        event.twitter_account_names = 'foo'
        self.assertEqual(event.build_twitter_search_query(), 'from:foo #baz')
        event.twitter_account_names = 'foo, @bar,@foobar'
        event.twitter_hashtags = 'baz,#quux , #bazquux'
        self.assertEqual(event.build_twitter_search_query(),
                         'from:foo OR from:bar OR from:foobar #baz OR #quux OR #bazquux')
        event.twitter_hashtags = ''
        self.assertEqual(event.build_twitter_search_query(), 'from:foo OR from:bar OR from:foobar')


class AttachmentModelTests(TestCase):
    fixtures = ['events_views_testdata']

    def tearDown(self):
        Attachment.objects.all().delete()  # not only delete DB entries but also the actual files from disk

    def test_repesentation(self):
        attachment = Attachment.objects.get(pk=1)
        self.assertEqual(repr(attachment), "<Attachment test.pdf for Test Event at 2016-07-20 by Person P>")

    def test_string_representation(self):
        attachment = Attachment.objects.get(pk=1)
        self.assertEqual(str(attachment), "test.pdf")

    @mock.patch('random.choice', lambda *args, **kwargs: 'x')
    def test_get_path_and_set_filename(self):
        attachment = Attachment.objects.get(pk=1)
        name = '/foo/bar/  baz    .TXT'
        path = attachment._get_path_and_set_filename(name)
        self.assertEqual(attachment.name, '  baz    .TXT')
        self.assertEqual(path, 'event_attachments/%s_baz_xxxxx.txt' % now().strftime("%Y/%m/%Y%m%d-%H%M"))

    @mock.patch('random.choice', lambda *args, **kwargs: 'x')
    def test_build_thumbnail(self):
        attachment = Attachment.objects.get(pk=1)
        self.assertEqual(attachment.thumbnail, "")
        attachment.attachment = SimpleUploadedFile(
            name='Lena.jpg',
            content=open(os.path.join(os.path.dirname(__file__), 'files', 'Lena.jpg'), 'rb').read(),
            content_type='image/jpeg')
        attachment.save()
        self.assertEqual(attachment.name, 'Lena.jpg')
        self.assertEqual(str(attachment.thumbnail),
                         'event_attachments/%s_Lena_xxxxx.thumbnail.jpg' % now().strftime("%Y/%m/%Y%m%d-%H%M"))
        self.assertTrue(os.path.exists(attachment.thumbnail.path))
        thumbnail = Image.open(attachment.thumbnail)
        self.assertEqual(thumbnail.height, attachment.MAX_HEIGHT)
        self.assertLess(thumbnail.width, attachment.MAX_WIDTH)

    def test_auto_delete_file_on_delete(self):
        event = Event.objects.get(pk=1)
        with tempfile.NamedTemporaryFile() as f1:
            attachment = Attachment(attachment=File(f1), event=event)
            attachment.save()
            file_path = attachment.attachment.path
            self.assertTrue(os.path.exists(file_path))
            attachment.delete()
            self.assertFalse(os.path.exists(file_path))

    def test_auto_delete_file_on_change_with_changed_attachment(self):
        event = Event.objects.get(pk=1)
        with tempfile.NamedTemporaryFile() as f1:
            attachment = Attachment(attachment=File(f1), event=event)
            attachment.save()
            old_file_path = attachment.attachment.path
            self.assertTrue(os.path.exists(old_file_path))
            with tempfile.NamedTemporaryFile() as f2:
                attachment.attachment = File(f2)
                attachment.save()
                new_file_path = attachment.attachment.path
                self.assertNotEqual(old_file_path, new_file_path)
                self.assertTrue(os.path.exists(new_file_path))
                self.assertFalse(os.path.exists(old_file_path))

    def test_auto_delete_file_on_change_with_unchanged_attachment(self):
        event = Event.objects.get(pk=1)
        with tempfile.NamedTemporaryFile() as f1:
            attachment = Attachment(attachment=File(f1), event=event)
            attachment.save()  # create attachment
            old_file_path = attachment.attachment.path
            self.assertTrue(os.path.exists(old_file_path))

            attachment.save()  # save unchanged attachment
            self.assertTrue(os.path.exists(old_file_path))
