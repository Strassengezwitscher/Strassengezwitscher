import os

from django.test import TestCase

from contact.models import Key
from contact.admin import KeyAdminForm


class AdminTests(TestCase):
    fixtures = ['gpg_key.json']

    def setUp(self):
        self.key = Key.objects.get(pk=1)

    def test_valid_key(self):
        """Test adding a valid GPG public key."""
        pub_key = self.key.key
        self.key.delete()
        form = KeyAdminForm({'key': pub_key})
        self.assertTrue(form.is_valid())

    def test_unique(self):
        """Test that adding a GPG public key twice leads to an error."""
        form = KeyAdminForm({'key': self.key.key})
        self.assertFalse(form.is_valid())
        self.assertTrue("exists" in form.errors['key'][0])

    def test_invalid_key(self):
        """Test that adding an invalid GPG public key leads to an error."""
        form = KeyAdminForm({'key': "some invalid public key"})
        self.assertFalse(form.is_valid())
        self.assertTrue("Invalid key." in form.errors['key'][0])

    def test_private_key(self):
        """Test that adding a GPG private key leads to an error."""
        file_path = os.path.join(os.path.dirname(__file__), 'files', 'private_key.asc')
        with open(file_path, 'r') as private_key_file:
            form = KeyAdminForm({'key': private_key_file.read()})
        self.assertFalse(form.is_valid())
        self.assertTrue("private" in form.errors['key'][0])
