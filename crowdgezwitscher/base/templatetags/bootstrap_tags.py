from django import template

register = template.Library()


@register.inclusion_tag('templatetags/bootstrap-errorlist.html')
def bootstrap_error_list(errors):
    return {
        'errors': errors,
    }


@register.inclusion_tag('templatetags/bootstrap-helptext.html')
def bootstrap_help_text(help_text):
    return {
        'help_text': help_text,
    }


@register.inclusion_tag('templatetags/bootstrap-field.html')
def bootstrap_field(field):
    return {
        'field': field,
    }


@register.inclusion_tag('templatetags/bootstrap-checkbox.html')
def bootstrap_checkbox(field):
    return {
        'field': field,
    }
