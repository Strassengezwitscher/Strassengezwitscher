from django import forms
import six

from .widgets import SelectizeSelectMultipleCSVInput


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
            if isinstance(elem, six.text_type) and elem.startswith(self.prefix):
                new_elems.append(elem.replace(self.prefix, '', 1))
            else:
                existing_elems.append(elem)
        self.new_elements = frozenset(new_elems)
        return super(ModelMultipleChoiceImplicitCreationField, self)._check_values(existing_elems)

    def save_new_elements(self):
        model = self.queryset.model
        new_objs = []
        for elem in self.new_elements:
            try:
                obj = model.objects.get(**{'%s' % self.attr_name: elem})
            except model.DoesNotExist:
                obj = model(**{'%s' % self.attr_name: elem})
                obj.clean()
                obj.save()
            new_objs.append(obj)
        return new_objs
