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


class BootstrapDatepicker(forms.widgets.DateInput):
    class Media:
        css = {
            'all': ('bootstrap-datepicker/dist/css/bootstrap-datepicker3.min.css',)
        }
        js = ('bootstrap-datepicker/dist/js/bootstrap-datepicker.js',)

    def render(self, name, value, attrs=None):
        attrs = {} if attrs is None else attrs
        attrs.update({'class': 'form-control'})
        html = super(BootstrapDatepicker, self).render(name, value, attrs)
        html = '<div class="input-group date" data-provide="datepicker" data-date-format="yyyy-mm-dd"> \
                %s \
                <div class="input-group-addon"> \
                    <span class="glyphicon glyphicon-th"></span> \
                </div> \
            </div>' % html
        return mark_safe(html)


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
