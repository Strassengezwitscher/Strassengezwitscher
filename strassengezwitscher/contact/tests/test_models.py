import os

from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction

from contact.models import Key
from contact.utils import GPGException


class KeyModelTests(TestCase):
    fixtures = ['gpg_key.json']

    def setUp(self):
        self.key = Key.objects.get(pk=1)

    def test_representation(self):
        self.assertEqual(repr(self.key), "<GPG Key for john.smith@example.org>")

    def test_string_representation(self):
        self.assertEqual(str(self.key), "GPG Key for john.smith@example.org")

    def test_add_same_key_twice(self):
        k = Key(key=self.key.key)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                k.save()
        self.assertEqual(Key.objects.count(), 1)

    def test_import_private_key(self):
        """Test if importing a GPG private key fails."""
        file_path = os.path.join(os.path.dirname(__file__), 'files', 'private_key.asc')
        with open(file_path, 'r') as private_key_file:
            k = Key(key=private_key_file.read()) 
        self.assertEqual(Key.objects.count(), 1)
        with self.assertRaises(GPGException):
            k.save()
        self.assertEqual(Key.objects.count(), 1)

    def test_import_broken_key(self):
        """Test if importing a broken GPG key fails."""
        k = Key(key="foobar")
        self.assertEqual(Key.objects.count(), 1)
        with self.assertRaises(GPGException):
            k.save()
        self.assertEqual(Key.objects.count(), 1)

    def test_email_address_extraction(self):
        """Test if corresponding email addresses are saved as well when saving a GPG public key."""
        self.key.addresses = ''
        self.assertEqual(self.key.addresses, '')
        self.key.save()
        self.assertEqual(self.key.addresses, 'john.smith@example.org')
