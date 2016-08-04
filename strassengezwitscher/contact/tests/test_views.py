import tempfile

from django.core import mail
from django.urls import reverse
from django.test import Client, TestCase
from django.test.utils import override_settings
from django.conf import settings

from contact.models import Key


@override_settings(EMAIL_BACKEND='contact.mail.GPGLocMemEmailBackend')
class ViewTests(TestCase):
    fixtures = ['gpg_key.json', 'user.json']

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        settings.EMAIL_TO_CONTACT_CONFIDENTIAL = ['john.smith@example.org']
        settings.EMAIL_TO_CONTACT_NON_CONFIDENTIAL = ['john.smith@example.org']

    def test_minimal_form(self):
        """
        Test sending required fields only. Message must be encrypted and be addressed to the non-confidential receivers.
        """
        settings.EMAIL_TO_CONTACT_CONFIDENTIAL = ['will.not.use.this@address.org']
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(reverse('contact:send_form'), {'subject': "Foo", 'message': "Bar"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(len(mail.outbox), 1)
        email = str(mail.outbox[0])
        self.assertTrue('BEGIN PGP MESSAGE' in email)
        self.assertTrue('Subject: Neue Nachricht von Streetcoverage' in email)
        self.assertTrue('From: %s' % settings.EMAIL_FROM_CONTACT in email)
        self.assertTrue('To: %s' % settings.EMAIL_TO_CONTACT_NON_CONFIDENTIAL[0] in email)
        self.assertTrue(settings.EMAIL_TO_CONTACT_CONFIDENTIAL[0] not in email)

    def test_confidential(self):
        """
        Test sending confidential message. Message must be encrypted and be addressed to the confidential receivers.
        """
        settings.EMAIL_TO_CONTACT_NON_CONFIDENTIAL = ['will.not.use.this@address.org']
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(reverse('contact:send_form'), {'subject': "Foo",
                                                                   'message': "Bar",
                                                                   'confidential': True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(len(mail.outbox), 1)
        email = str(mail.outbox[0])
        self.assertTrue('BEGIN PGP MESSAGE' in email)
        self.assertTrue('Subject: Neue Nachricht von Streetcoverage' in email)
        self.assertTrue('From: %s' % settings.EMAIL_FROM_CONTACT in email)
        self.assertTrue('To: %s' % settings.EMAIL_TO_CONTACT_CONFIDENTIAL[0] in email)
        self.assertTrue(settings.EMAIL_TO_CONTACT_NON_CONFIDENTIAL[0] not in email)

    def test_attachment(self):
        """
        Test sending contact form including a file. Message must be encrypted and be addressed to the non-confidential
        receivers. As the message is encrypted we cannot directly check for the file being attached.
        """
        settings.EMAIL_TO_CONTACT_CONFIDENTIAL = ['will.not.use.this@address.org']
        attachment_name = "dolphin_diary"
        attachment_content = "Thanks for all the fish.".encode('utf-8')

        self.assertEqual(len(mail.outbox), 0)
        with tempfile.NamedTemporaryFile(prefix=attachment_name) as f:
            f.write(attachment_content)
            f.seek(0)
            response = self.client.post(reverse('contact:send_form'), {'subject': "Foo",
                                                                       'message': "Bar",
                                                                       'files': f})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(len(mail.outbox), 1)
        email = str(mail.outbox[0])
        self.assertTrue('BEGIN PGP MESSAGE' in email)
        self.assertTrue('Subject: Neue Nachricht von Streetcoverage' in email)
        self.assertTrue('From: %s' % settings.EMAIL_FROM_CONTACT in email)
        self.assertTrue('To: %s' % settings.EMAIL_TO_CONTACT_NON_CONFIDENTIAL[0] in email)
        self.assertTrue(settings.EMAIL_TO_CONTACT_CONFIDENTIAL[0] not in email)

    def test_multiple_attachments_with_one_as_text(self):
        """
        Test sending contact form including two files. Message must be encrypted and be addressed to the
        non-confidential receivers. As the message is encrypted we cannot directly check for the files being attached.
        The first attachment's decoding is tested, the other shall not be decoded as its content_type is not text.
        """
        settings.EMAIL_TO_CONTACT_CONFIDENTIAL = ['will.not.use.this@address.org']
        attachment_name = "dolphin_diary"
        attachment_content = "Thanks for all the fish.".encode('utf-8')

        self.assertEqual(len(mail.outbox), 0)
        with tempfile.NamedTemporaryFile(prefix=attachment_name, suffix='.txt') as f:
            f.write(attachment_content)
            f.seek(0)
            with tempfile.NamedTemporaryFile(prefix=attachment_name) as g:
                g.write(attachment_content)
                g.seek(0)
                response = self.client.post(reverse('contact:send_form'), {'subject': "Foo",
                                                                           'message': "Bar",
                                                                           'files': [f, g]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(len(mail.outbox), 1)
        email = str(mail.outbox[0])
        self.assertTrue('BEGIN PGP MESSAGE' in email)
        self.assertTrue('Subject: Neue Nachricht von Streetcoverage' in email)
        self.assertTrue('From: %s' % settings.EMAIL_FROM_CONTACT in email)
        self.assertTrue('To: %s' % settings.EMAIL_TO_CONTACT_NON_CONFIDENTIAL[0] in email)
        self.assertTrue(settings.EMAIL_TO_CONTACT_CONFIDENTIAL[0] not in email)

    def test_incomplete_data(self):
        """Test sending not all required fields."""
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(reverse('contact:send_form'), {'subject': "Foo"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')
        self.assertEqual(response.json()['errors'], {'message': ["This field is required."]})
        self.assertEqual(len(mail.outbox), 0)

    def test_invalid_data(self):
        """Test sending forbidden values."""
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(reverse('contact:send_form'),
                                    {'subject': "Foo", 'message': "Bar",
                                     'name': 'a' * 51})  # too long
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')
        self.assertTrue('at most 50 characters' in response.json()['errors']['name'][0])
        self.assertEqual(len(mail.outbox), 0)

    def test_invalid_attachment_file_name(self):
        """Test sending single attachment with overlong file name."""
        attachment_name = 'a' * 51  # too long
        attachment_content = "Thanks for all the fish.".encode('utf-8')

        self.assertEqual(len(mail.outbox), 0)
        with tempfile.NamedTemporaryFile(prefix=attachment_name) as f:
            f.write(attachment_content)
            f.seek(0)
            response = self.client.post(reverse('contact:send_form'), {'subject': "Foo",
                                                                       'message': "Bar",
                                                                       'files': f})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')
        self.assertTrue('at most 50 characters' in response.json()['errors']['files'][0])
        self.assertEqual(len(mail.outbox), 0)

    def test_valid_and_invalid_attachment_file_name1(self):
        """Test sending two attachments. One has an overlong file name. Send the valid file first."""
        attachment_name1 = "dolphin_diary"
        attachment_name2 = 'a' * 51  # too long
        attachment_content = "Thanks for all the fish.".encode('utf-8')

        self.assertEqual(len(mail.outbox), 0)
        with tempfile.NamedTemporaryFile(prefix=attachment_name1) as f:
            f.write(attachment_content)
            f.seek(0)
            with tempfile.NamedTemporaryFile(prefix=attachment_name2) as g:
                g.write(attachment_content)
                g.seek(0)
                response = self.client.post(reverse('contact:send_form'), {'subject': "Foo",
                                                                           'message': "Bar",
                                                                           'files': [f, g]})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')
        self.assertTrue('at most 50 characters' in response.json()['errors']['files'][0])
        self.assertEqual(len(mail.outbox), 0)

    def test_valid_and_invalid_attachment_file_name2(self):
        """Test sending two attachments. One has an overlong file name. Send the invalid file first."""
        attachment_name1 = 'a' * 51  # too long
        attachment_name2 = "dolphin_diary"
        attachment_content = "Thanks for all the fish.".encode('utf-8')

        self.assertEqual(len(mail.outbox), 0)
        with tempfile.NamedTemporaryFile(prefix=attachment_name1) as f:
            f.write(attachment_content)
            f.seek(0)
            with tempfile.NamedTemporaryFile(prefix=attachment_name2) as g:
                g.write(attachment_content)
                g.seek(0)
                response = self.client.post(reverse('contact:send_form'), {'subject': "Foo",
                                                                           'message': "Bar",
                                                                           'files': [f, g]})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')
        self.assertTrue('at most 50 characters' in response.json()['errors']['files'][0])
        self.assertEqual(len(mail.outbox), 0)

    def test_missing_public_key(self):
        """Test returned error message when no GPG public key is present for the chosen recipient(s)."""
        for key in Key.objects.all():
            key.delete()
        settings.EMAIL_TO_CONTACT_CONFIDENTIAL = ['will.not.use.this@address.org']
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(reverse('contact:send_form'), {'subject': "Foo", 'message': "Bar"})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['status'], 'error')
        self.assertEqual(response.json()['errors'], "Email could not be sent.")
        self.assertEqual(len(mail.outbox), 0)

    def test_csrf_token_not_required(self):
        """Test that no CSRF token is required to access the view, irrespective of the user begin logged in or not."""
        # not logged in
        response = self.client.post(reverse('contact:send_form'), {'subject': "Foo", 'message': "Bar"})
        self.assertEqual(response.status_code, 200)

        self.client.login(username='user', password='password')

        # logged in
        response = self.client.post(reverse('contact:send_form'), {'subject': "Foo", 'message': "Bar"})
        self.assertEqual(response.status_code, 200)

    def test_get(self):
        """Test if endpoint is not available via GET."""
        response = self.client.get(reverse('contact:send_form'))
        self.assertEqual(response.status_code, 405)
