from django import forms
from django.utils.safestring import mark_safe


class SelectizeSelectMultiple(forms.widgets.SelectMultiple):
    class Media:
        css = {
            'all': ('selectize/dist/css/selectize.bootstrap3.css',)
        }
        js = ('selectize/dist/js/standalone/selectize.min.js',)

    def render(self, name, value, attrs=None):
        value = [] if not value else value
        html = super(SelectizeSelectMultiple, self).render(name, value, attrs)
        script = '<script type="text/javascript"> \
                $(function() { \
                    $("#%s").selectize({ \
                        plugins: ["remove_button"], \
                        items: %s \
                    });\
                });\
            </script>' % (attrs['id'], '[%s]' % ','.join(map(str, value)))
        return mark_safe(''.join(html + script))
