from decimal import Decimal

from django.core import exceptions
from django.db import models, transaction
from django.test import TestCase

from base.fields import RoundingDecimalField, UnsignedBigIntegerField


class RoundingDecimalFieldTests(TestCase):
    field = RoundingDecimalField(max_digits=9, decimal_places=6)

    def test_data_normal(self):
        self.assertEqual(self.field.to_python('11.123456'), Decimal('11.123456'))

    def test_data_too_short(self):
        self.assertEqual(self.field.to_python('11.1234'), Decimal('11.123400'))

    def test_data_too_long(self):
        self.assertEqual(self.field.to_python('11.12345678'), Decimal('11.123457'))


class UnsignedBigIntegerModel(models.Model):
    value = UnsignedBigIntegerField()
    null_value = UnsignedBigIntegerField(null=True, blank=True)


class UnsignedBigIntegerFieldTests(TestCase):
    model = UnsignedBigIntegerModel
    documented_range = (0, 2 ** 64 - 1)

    def test_formfield(self):
        field = UnsignedBigIntegerField()
        self.assertEqual(field.formfield().min_value, 0)
        self.assertEqual(field.formfield().max_value, 2 ** 64 - 1)

    # The following tests are inspired from Django's own internal tests which are not part of the Django package in pip.
    # See: https://github.com/django/django/blob/master/tests/model_fields/test_integerfield.py

    def test_documented_range(self):
        """
        Values within the documented safe range pass validation, and can be
        saved and retrieved without corruption.
        """
        min_value, max_value = self.documented_range

        instance = self.model(value=min_value)
        instance.full_clean()
        instance.save()
        qs = self.model.objects.filter(value__lte=min_value)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].value, min_value)

        instance = self.model(value=max_value)
        instance.full_clean()
        instance.save()
        qs = self.model.objects.filter(value__gte=max_value)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].value, max_value)

    def test_outside_documented_range(self):
        """
        Values outside the documented safe range cannot be saved.
        """
        min_value, max_value = self.documented_range

        instance = self.model(value=min_value - 1)
        with self.assertRaises(exceptions.ValidationError):
            with transaction.atomic():
                instance.save()
        qs = self.model.objects.filter(value__lte=min_value)
        self.assertEqual(qs.count(), 0)

        instance = self.model(value=max_value + 1)
        with self.assertRaises(exceptions.ValidationError):
            with transaction.atomic():
                instance.save()
        qs = self.model.objects.filter(value__gte=max_value)
        self.assertEqual(qs.count(), 0)

    def test_types(self):
        instance = self.model(value=0)
        self.assertIsInstance(instance.value, int)
        instance.save()
        self.assertIsInstance(instance.value, int)
        instance = self.model.objects.get()
        self.assertIsInstance(instance.value, int)

    def test_coercing(self):
        self.model.objects.create(value='10')
        instance = self.model.objects.get(value='10')
        self.assertEqual(instance.value, 10)
