import json

from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape


class SelectizeSelectMultiple(forms.widgets.SelectMultiple):
    class Media:
        css = {
            'all': ('selectize/dist/css/selectize.bootstrap3.css',)
        }
        js = ('selectize/dist/js/standalone/selectize.min.js',)

    def render(self, name, value, attrs=None):
        html = super(SelectizeSelectMultiple, self).render(name, value, attrs)
        value = value or []
        script = '<script type="text/javascript"> \
                $(function() { \
                    $("#%s").selectize({ \
                        plugins: ["remove_button"], \
                        items: %s \
                    }); \
                }); \
            </script>' % (attrs['id'], '[%s]' % ','.join(map(str, value)))
        return mark_safe(''.join(html + script))


class SelectizeSelectMultipleCSVInput(forms.widgets.SelectMultiple):
    """
    A selectize.js widget that allows selecting multiple existing values and adding new values.

    New values are prefixed with the value supplied by the prefix construction parameter.
    """
    class Media:
        css = {
            'all': ('selectize/dist/css/selectize.bootstrap3.css',)
        }
        js = ('selectize/dist/js/standalone/selectize.min.js',)

    def __init__(self, prefix, *args, **kwargs):
        super(SelectizeSelectMultipleCSVInput, self).__init__(*args, **kwargs)
        self.prefix = prefix

    def render(self, name, value, attrs=None):
        html = super(SelectizeSelectMultipleCSVInput, self).render(name, value, attrs)
        value = value or []
        script = '<script type="text/javascript"> \
                $(function() { \
                    $("#%s").selectize({ \
                        plugins: ["remove_button"], \
                        items: %s, \
                        create: function(input) { \
                            return { \
                                value: \"%s\" + input, \
                                text: input \
                            } \
                        } \
                    }); \
                }); \
            </script>' % (attrs['id'], '["%s"]' % '","'.join(map(str, value)), self.prefix)
        return mark_safe(''.join(html + script))


class SelectizeCSVInput(forms.widgets.TextInput):
    class Media:
        css = {
            'all': ('selectize/dist/css/selectize.bootstrap3.css',)
        }
        js = ('selectize/dist/js/standalone/selectize.min.js',)

    def render(self, name, value, attrs=None):
        html = super(SelectizeCSVInput, self).render(name, value, attrs)
        value = value or ''
        script = '<script type="text/javascript"> \
                $(function() { \
                    $("#%s").selectize({ \
                        plugins: ["remove_button"], \
                        items: %s, \
                        create: function(input) { \
                            return { \
                                value: input, \
                                text: input \
                            } \
                        } \
                    }); \
                }); \
            </script>' % (attrs['id'], '["%s"]' % value.replace(',', '","'))
        return mark_safe(''.join(html + script))


class BootstrapPicker(object):
    class Media:
        css = {
            'all': ('eonasdan-bootstrap-datetimepicker/build/css/bootstrap-datetimepicker.min.css',)
        }
        js = (
            'moment/min/moment-with-locales.min.js',
            'eonasdan-bootstrap-datetimepicker/build/js/bootstrap-datetimepicker.min.js',
        )

    def render(self, name, value, attrs=None):
        attrs = {} if attrs is None else attrs
        attrs.update({'class': 'form-control'})
        html = super(BootstrapPicker, self).render(name, value, attrs)
        html = '<div class="input-group date"> \
                %s \
                <div class="input-group-addon"> \
                    <span class="glyphicon glyphicon-calendar"></span> \
                </div> \
            </div>' % html
        html += '<script type="text/javascript"> \
            $(function() { \
                $("#%s").datetimepicker(%s); \
           }); \
        </script>' % (attrs['id'], json.dumps(self.config()))
        return mark_safe(html)

    def config(self):
        return {
            'locale': 'de',
            'showClose': True,
            'useCurrent': False,
        }


class ClearableBootstrapPickerMixin(object):
    def config(self):
        config = super(ClearableBootstrapPickerMixin, self).config()
        config.update({'showClear': True})
        return config


class BootstrapDatePicker(BootstrapPicker, forms.widgets.DateInput):
    def config(self):
        config = super(BootstrapDatePicker, self).config()
        config.update({
            'viewMode': 'days',
            'format': 'YYYY-MM-DD',
        })
        return config


class BootstrapTimePicker(BootstrapPicker, forms.widgets.DateInput):
    def config(self):
        config = super(BootstrapTimePicker, self).config()
        config.update({
            'format': 'HH:mm',
        })
        return config


class ClearableBootstrapDatePicker(ClearableBootstrapPickerMixin, BootstrapDatePicker):
    pass


class ClearableBootstrapTimePicker(ClearableBootstrapPickerMixin, BootstrapTimePicker):
    pass


class AttachmentInput(forms.widgets.ClearableFileInput):
    template_with_initial = (
        '<br />%(initial_text)s: <a href="%(initial_url)s">%(initial)s</a> '
        '%(clear_template)s<br />'
        '<div style="float:left; margin-right:10px;">%(input_text)s:</div>'
        '<span style="display: block; overflow: hidden;">%(input)s</span>'
    )

    def get_template_substitution_values(self, value):
        """Show attachment's name instead of its URL."""
        return {
            'initial': conditional_escape(value.instance.name),
            'initial_url': conditional_escape(value.url),
        }
