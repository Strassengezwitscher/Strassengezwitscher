from decimal import Decimal

from django import forms
from django.db import models


def round_decimal(value, places):
    if value is not None:
        return value.quantize(Decimal(10) ** -places)
    return value


class RoundingDecimalField(forms.DecimalField):
    def to_python(self, value):
        value = super(RoundingDecimalField, self).to_python(value)
        return round_decimal(value, self.decimal_places)
