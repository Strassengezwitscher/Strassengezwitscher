from decimal import Decimal

from django.test import TestCase

from crowdgezwitscher.fields import RoundingDecimalField


class RoundingDecimalFieldTests(TestCase):
    field = RoundingDecimalField(max_digits=9, decimal_places=6)

    def test_data_normal(self):
        self.assertEqual(self.field.to_python('11.123456'), Decimal('11.123456'))

    def test_data_too_short(self):
        self.assertEqual(self.field.to_python('11.1234'), Decimal('11.123400'))

    def test_data_too_long(self):
        self.assertEqual(self.field.to_python('11.12345678'), Decimal('11.123457'))
