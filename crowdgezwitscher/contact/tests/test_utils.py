import os

from django.test import TestCase
from gnupg import GPG

from contact.models import Key
from contact.utils import TemporaryDirectory, GPGException, addresses_for_key, handle_gpg_error


class UtilTests(TestCase):
    fixtures = ['gpg_key.json']

    def setUp(self):
        self.key = Key.objects.get(pk=1)

    def test_temp_dir_gets_deleted(self):
        """
        Test if a temporary directory created by TemporaryDirectory() is deleted after leaving the context manager.
        """
        with TemporaryDirectory() as temp_dir:
            self.assertTrue(os.path.isdir(temp_dir))
            self.assertFalse(os.path.isfile(temp_dir))
        self.assertFalse(os.path.isdir(temp_dir))
        self.assertFalse(os.path.isfile(temp_dir))

    def test_addresses_for_key(self):
        """Test email address extraction from GPG public keys."""
        with TemporaryDirectory() as temp_dir:
            gpg_keychain = GPG(gnupghome=temp_dir)
            res = gpg_keychain.import_keys(self.key.key)
            self.assertTrue(res)
            self.assertEqual(len(res.results), 1)
            self.assertEqual(addresses_for_key(gpg_keychain, res.results[0]), ['john.smith@example.org'])

    def test_handle_gpg_error(self):
        """Test if helper function raises a GPGException."""
        result = {'status': 'Failed horribly', 'stderr': 'Segfault'}
        operation = "Div0"
        with self.assertRaises(GPGException):
            handle_gpg_error(result, operation)
