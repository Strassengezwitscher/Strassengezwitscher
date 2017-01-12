from django import template

register = template.Library()


@register.inclusion_tag('templatetags/errorlist.html')
def bootstrap_error_list(errors):
    return {
        'errors': errors,
    }
