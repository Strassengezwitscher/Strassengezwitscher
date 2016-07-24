from django.test import TestCase

from contact.mail import GPGEmailMessage
from contact.utils import GPGException


class MailTests(TestCase):
    fixtures = ['gpg_key.json']

    def test_basic_encrypt(self):
        """Test if PGP/MIME format requirements look fulfilled and if headers are correct."""
        subject = "Dear friend, special offer for you"
        body = "Buy cheap viagra"
        from_address = "cheap@viagra.biz"
        to_addresses = ["john.smith@example.org"]
        email = GPGEmailMessage(subject, body, from_address, to_addresses)
        self.assertEqual(email.subject, subject)
        self.assertEqual(email.body, body)
        self.assertEqual(email.from_email, from_address)
        self.assertEqual(email.to, to_addresses)
        self.assertEqual(email.recipients(), to_addresses)
        email = str(email.message())
        self.assertTrue('Content-Type: multipart/encrypted;' in email)
        self.assertTrue('protocol="application/pgp-encrypted";' in email)
        self.assertTrue('Content-Type: application/pgp-encrypted' in email)
        self.assertTrue('Content-Type: application/octet-stream; name="encrypted.asc"' in email)
        self.assertTrue('Content-Disposition: inline; filename="encrypted.asc"' in email)
        self.assertTrue('Content-Description: OpenPGP encrypted message' in email)
        self.assertTrue('Content-Description: PGP/MIME Versions Identification' in email)
        self.assertEqual(email.count('Content-Transfer-Encoding: 7bit'), 3)
        self.assertTrue('Subject: %s' % subject in email)
        self.assertTrue('BEGIN PGP MESSAGE' in email)
        self.assertTrue('From: %s' % from_address in email)
        self.assertTrue('To: %s' % to_addresses[0] in email)

    def test_encrypt_with_attachment(self):
        """
        Test if PGP/MIME format requirements look fulfilled and if headers are correct when an attachment is present.
        As the message is encrypted we cannot directly check for the file being attached.
        """
        subject = "Dear friend, special offer for you"
        body = "Buy cheap viagra"
        from_address = "cheap@viagra.biz"
        to_addresses = ["john.smith@example.org"]
        email = GPGEmailMessage(subject, body, from_address, to_addresses)

        self.assertEqual(len(email.attachments), 0)
        attachment_name = "dolphin_diary.txt"
        attachment_content = "Thanks for all the fish."
        email.attach(attachment_name, attachment_content)

        self.assertEqual(len(email.attachments), 1)
        self.assertEqual(email.attachments[0][0], attachment_name)
        self.assertEqual(email.attachments[0][1], attachment_content)

        email = str(email.message())

        self.assertTrue('Content-Type: multipart/encrypted;' in email)
        self.assertTrue('protocol="application/pgp-encrypted";' in email)
        self.assertTrue('Content-Type: application/pgp-encrypted' in email)
        self.assertTrue('Content-Type: application/octet-stream; name="encrypted.asc"' in email)
        self.assertTrue('Content-Disposition: inline; filename="encrypted.asc"' in email)
        self.assertTrue('Content-Description: OpenPGP encrypted message' in email)
        self.assertTrue('Content-Description: PGP/MIME Versions Identification' in email)
        self.assertEqual(email.count('Content-Transfer-Encoding: 7bit'), 3)
        self.assertTrue('Subject: %s' % subject in email)
        self.assertTrue('BEGIN PGP MESSAGE' in email)
        self.assertTrue('From: %s' % from_address in email)
        self.assertTrue('To: %s' % to_addresses[0] in email)

    def test_encrypt_with_two_attachments(self):
        """
        Test if PGP/MIME format requirements look fulfilled and if headers are correct when two attachments are present.
        As the message is encrypted we cannot directly check for the files being attached.
        """
        subject = "Dear friend, special offer for you"
        body = "Buy cheap viagra"
        from_address = "cheap@viagra.biz"
        to_addresses = ["john.smith@example.org"]
        email = GPGEmailMessage(subject, body, from_address, to_addresses)

        self.assertEqual(len(email.attachments), 0)
        attachment_name1 = "dolphin_diary.txt"
        attachment_name2 = "ancient_dolphin_diary.txt"
        attachment_content = "Thanks for all the fish."
        email.attach(attachment_name1, attachment_content)
        email.attach(attachment_name2, attachment_content)

        self.assertEqual(len(email.attachments), 2)
        self.assertEqual(email.attachments[0][0], attachment_name1)
        self.assertEqual(email.attachments[0][1], attachment_content)
        self.assertEqual(email.attachments[1][0], attachment_name2)
        self.assertEqual(email.attachments[1][1], attachment_content)

        email = str(email.message())

        self.assertTrue('Content-Type: multipart/encrypted;' in email)
        self.assertTrue('protocol="application/pgp-encrypted";' in email)
        self.assertTrue('Content-Type: application/pgp-encrypted' in email)
        self.assertTrue('Content-Type: application/octet-stream; name="encrypted.asc"' in email)
        self.assertTrue('Content-Disposition: inline; filename="encrypted.asc"' in email)
        self.assertTrue('Content-Description: OpenPGP encrypted message' in email)
        self.assertTrue('Content-Description: PGP/MIME Versions Identification' in email)
        self.assertEqual(email.count('Content-Transfer-Encoding: 7bit'), 3)
        self.assertTrue('Subject: %s' % subject in email)
        self.assertTrue('BEGIN PGP MESSAGE' in email)
        self.assertTrue('From: %s' % from_address in email)
        self.assertTrue('To: %s' % to_addresses[0] in email)

    def test_encrypt_missing_public_key(self):
        """
        Test if a missing GPG public key for at least one receiver leads to an error and the email not being sent.
        """
        subject = "Dear friend, special offer for you"
        body = "Buy cheap viagra"
        from_address = "cheap@viagra.biz"
        to_addresses = ["john.smith@example.org", "unknown@person.com"]
        email = GPGEmailMessage(subject, body, from_address, to_addresses)
        self.assertEqual(len(email.attachments), 0)
        self.assertEqual(email.body, body)
        self.assertEqual(email.to, to_addresses)
        self.assertEqual(email.recipients(), to_addresses)
        with self.assertRaises(GPGException):
            email.send()
        self.assertEqual(len(email.attachments), 0)

    def test_additional_mail_headers(self):
        """
        Test if some mail headers we do not use still work.
        We have overriden the method that is responsible for them and do not want to break existing functionality.
        """
        subject = "Dear friend, special offer for you"
        body = "Buy cheap viagra"
        from_address = "change@me.com"
        to_addresses = ["john.smith@example.org"]
        cc_addresses = ["john.smith@example.org"]
        bcc_addresses = ["john.smith@example.org"]
        reply_to_addresses = ["another@address.org"]
        second_from_address = 'cheap@viagra.biz'
        email = GPGEmailMessage(subject, body, from_address, to_addresses,
                                cc=cc_addresses, bcc=bcc_addresses, reply_to=reply_to_addresses)
        email.extra_headers['Foo'] = 'Bar'
        email.extra_headers['From'] = second_from_address
        self.assertEqual(email.subject, subject)
        self.assertEqual(email.body, body)
        self.assertEqual(email.from_email, from_address)
        self.assertEqual(email.recipients().sort(), (to_addresses + cc_addresses + bcc_addresses).sort())
        email = str(email.message())
        self.assertTrue('Content-Type: multipart/encrypted;' in email)
        self.assertTrue('protocol="application/pgp-encrypted";' in email)
        self.assertTrue('Content-Type: application/pgp-encrypted' in email)
        self.assertTrue('Content-Type: application/octet-stream; name="encrypted.asc"' in email)
        self.assertTrue('Content-Disposition: inline; filename="encrypted.asc"' in email)
        self.assertTrue('Content-Description: OpenPGP encrypted message' in email)
        self.assertTrue('Content-Description: PGP/MIME Versions Identification' in email)
        self.assertEqual(email.count('Content-Transfer-Encoding: 7bit'), 3)
        self.assertTrue('Subject: %s' % subject in email)
        self.assertTrue('BEGIN PGP MESSAGE' in email)
        self.assertTrue('From: %s' % second_from_address in email)
        self.assertTrue('To: %s' % to_addresses[0] in email)
        self.assertTrue('Cc: %s' % cc_addresses[0] in email)
        self.assertTrue('Reply-To: %s' % reply_to_addresses[0] in email)
        self.assertTrue('Foo: Bar' in email)
        self.assertEqual(email.count('From:'), 1)
