from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from gnupg import GPG

from strassengezwitscher.log import logger
from contact.utils import GPGException, TemporaryDirectory, addresses_for_key, handle_gpg_error


@python_2_unicode_compatible
class Key(models.Model):
    """Stores a GPG public key and the corresponding email addresses extracted from it."""
    key = models.TextField(unique=True)
    addresses = models.TextField(editable=False)

    def __repr__(self):
        return "<GPG Key for " + self.addresses + ">"

    def __str__(self):
        return "GPG Key for " + self.addresses

    def save(self, *args, **kwargs):
        with TemporaryDirectory() as temp_dir:
            gpg_keychain = GPG(gnupghome=temp_dir)
            res = gpg_keychain.import_keys(self.key)
            if not res:
                handle_gpg_error(res, 'import')
            if len(gpg_keychain.list_keys(True)) > 0:
                raise GPGException("Will not import GPG private key!")
            addresses = []
            for key in res.results:
                addresses.extend(addresses_for_key(gpg_keychain, key))
            self.addresses = ', '.join(addresses)
        operation = "Updating" if self.pk else "Creating"
        logger.info("%s GPG key for: %s", operation, self.addresses)
        super(Key, self).save(*args, **kwargs)
