from decimal import Decimal

from django import forms
from django.core import exceptions
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .widgets import SelectizeSelectMultipleCSVInput


##############
# Model fields
##############
class UnsignedBigIntegerField(models.BigIntegerField):
    """A 64 bit field storing unsigned integers from 0 to 18446744073709551615."""
    description = "Big (8 byte) unsigned integer"
    MAX_BIGINT = 18446744073709551615
    default_error_messages = {
        'invalid': _("'%(value)s' value must be an integer ≥ 0 and ≤ 18446744073709551615."),
    }

    def formfield(self, **kwargs):
        defaults = {'min_value': 0,
                    'max_value': UnsignedBigIntegerField.MAX_BIGINT}
        defaults.update(kwargs)
        return super(UnsignedBigIntegerField, self).formfield(**defaults)

    def from_db_value(self, value, *_):
        if value is None:
            return value
        return value + 2 ** 63

    def get_prep_value(self, value):
        if value is None:
            return value
        try:
            value = int(value)
            if value < 0 or value > self.MAX_BIGINT:
                raise ValueError
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )
        return value - 2 ** 63



#############
# Form fields
#############
def round_decimal(value, places):
    if value is not None:
        return value.quantize(Decimal(10) ** -places)
    return value


class RoundingDecimalField(forms.DecimalField):
    def to_python(self, value):
        value = super(RoundingDecimalField, self).to_python(value)
        return round_decimal(value, self.decimal_places)


class ModelMultipleChoiceImplicitCreationField(forms.ModelMultipleChoiceField):
    """
    A ModelMultipleChoiceField that allows implicitly creating new model instances.

    Besides allowing references to existing model instances, valid choices include str values starting with a supplied
    prefix.
    When creating the new model instance, the remaining value behind the prefix is passed to the model constructor as
    the field specified by the supplied value for attr_name.
    """
    widget = SelectizeSelectMultipleCSVInput

    def __init__(self, queryset, prefix, attr_name, *args, **kwargs):
        widget = self.widget(prefix=prefix)
        super(ModelMultipleChoiceImplicitCreationField, self).__init__(queryset, widget=widget, *args, **kwargs)
        self.prefix = prefix
        self.attr_name = attr_name

    def clean(self, value):
        qs = super(ModelMultipleChoiceImplicitCreationField, self).clean(value)
        new_elements = self.save_new_elements()
        return list(qs) + new_elements

    def _check_values(self, value):
        # this method is called by clean()
        existing_elems = []
        new_elems = []
        for elem in value:
            if isinstance(elem, str) and elem.startswith(self.prefix):
                new_elems.append(elem.replace(self.prefix, '', 1))
            else:
                existing_elems.append(elem)
        self.new_elements = frozenset(new_elems)
        return super(ModelMultipleChoiceImplicitCreationField, self)._check_values(existing_elems)

    def save_new_elements(self):
        new_objs = []
        if hasattr(self, 'new_elements'):
            model = self.queryset.model
            for elem in self.new_elements:
                try:
                    obj = model.objects.get(**{'%s' % self.attr_name: elem})
                except model.DoesNotExist:
                    obj = model(**{'%s' % self.attr_name: elem})
                    obj.clean()
                    obj.save()
                new_objs.append(obj)
        return new_objs
