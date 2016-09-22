from django import forms
from django.utils.safestring import mark_safe


class SelectizeSelectMultiple(forms.widgets.SelectMultiple):
    class Media:
        css = {
            'all': ('selectize/dist/css/selectize.bootstrap3.css',)
        }
        js = ('selectize/dist/js/standalone/selectize.min.js',)

    def render(self, name, value, attrs=None):
        html = super(SelectizeSelectMultiple, self).render(name, value, attrs)
        value = [] if not value else value
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
        value = '' if not value else value
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
