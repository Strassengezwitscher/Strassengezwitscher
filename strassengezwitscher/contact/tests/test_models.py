from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction

from contact.models import Key
from contact.utils import GPGException

private_key = """
-----BEGIN PGP PRIVATE KEY BLOCK-----
Comment: GPGTools - http://gpgtools.org

lQHYBFeGeIEBBADZ9Z30ILsZ5BnsonPouq0wUIq3cDJFOvX0D04Z63FyHHz2wg/1
gfXJE635bMapRhFvPArBEuVO/E4CqEENruJczAWg9IqTMHOmcvhHrTvbEt87mWbX
H1X1k3nwLPlQeUPaVrB+RZs5z9BJuqj21sYJ4337sErSLi5okFPC08H1kQARAQAB
AAP/UUlGZskcLkxBFN0DQFz6gSXQjhgkT2htWN+qX4VM0mNogXifjg6xVRPnUrns
Hy44C1WHpzj+VyZGi7wnQsyhs4zY491Mktj5B3s1u+bSd60wP7DtFCCC8rx/rsY1
q6Yjf5H1P4vsDQKCXUCnW1YV4gFrbJzzkqPsjC+uDlmtHZcCAOlYFET9MBDmfZBI
UDFqFKjz5ls2lSVvbXz3nQiSAWp0qlcaMwB9Gi+RBCs8kWToWLG2qkpDjSrDtMGI
lwmsm28CAO8fJJqOzg09KkP7tU2dY7CFHQRHvWaVRDzsXE7dnS9x2gHkrRMGWSoI
pwE7jmCzuigyFDil3EtgWljZR3mV/v8B/2KOpkJjwKQZj9n31MvetItv7/529HZH
9saDA5AJS20CtgINmnDAdemWrcLECfmqhTGlHxWHe6BfgkCyePSCqCSZB7QjSm9o
biBTbWl0aCA8am9obi5zbWl0aEBleGFtcGxlLm9yZz6IuQQTAQgAIwUCV4Z4gQIb
AwcLCQgHAwIBBhUIAgkKCwQWAgMBAh4BAheAAAoJEG/iYSB8Pf2bkwwD/ArdFBon
zl70fvUXpR82dq5V+Cb2XO26HnnCWAeW2swwSCc+dXWJ3zID0Wq9ZZK5JZK53fQO
I3dQeQ1kN2DwWTLraMSdjZYGkQlzAChZUbBz3mQ5X203kFa/moLzcTS24Odzh4Yf
JkdVOVMqQjADxP0P1RUxVE2dEybWrVTCPgzrnQHYBFeGeIEBBACtHCrjxbzqO4HR
OpHPY8556KJnctExaRAKyde3xXI/weLlos1e576a8ijZJE+cLeOt4K3Oh1oqWhML
rv/iQ2RDKgy+6djtr7lP+GaBBH0teBwMy3zV8L/BW54uDmFEK1tS3l2Dmfw1JsOO
aXiToDBnWJ4lgt2siH3liUVC1VzpswARAQABAAP5AREFEdMZfHlFgy788jlGuLSG
7qJQB6owA8IRNE/moKrF5wP2IQ3izUlaG2I6tQSomgIOJhyrwu9vQrynu9m4ywsT
PqMRwFTLC1F6vygu/vid+tXIs/gL0p3cF4MCuZfJyWIK7WmIS1ucunLWjQ9pSvRq
rVwghqZ5pVFdV5WHYLECAM4GL6ilewDFzPwrERlzpu7UkWIwKHeMVDhRGe2N0a/z
QMPQu0fAbqEw3Swo3A8XZJQY7tR+2vxhBRaj5BhJnesCANcaDzQa0YQFSv987qi0
Fa6B+oLpeNoBB3Daj0P/1AZ8s9oEvNBpZdbqefGXo+SYpRWvsgzGXaDyf6hNnBj3
SVkB/igsKWHxfGMXAG22m+68wmoQwO1/zFwquDL7mqefLkBZxbrorYPhjw6VSdUO
s+vKLNGiqJquVcMsUHA9YD0Z9DyihoifBBgBCAAJBQJXhniBAhsMAAoJEG/iYSB8
Pf2bITkEANebrvCz5pAS53opkEkfGwZg2S9G2lSCd/pMa3vqqudRHZHq1qNEM3wk
wBry9nZrpAQZuHWm28G314oOmtZFiuZK+VEAsMl7L1kyg/kLi/BaEFxcFV42lZEp
C1nRrBCOnw8SLZRvWkfK7WrM4qbwA6KsvpL14i1414fleYXoCMib
=L3F6
-----END PGP PRIVATE KEY BLOCK-----
"""


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
        k = Key(key=private_key)
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
