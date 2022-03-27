from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def split(string, sep):
    """Return the string split by sep.

    Example usage: {{ value|split:"/" }}
    """
    return string.split(sep)


@stringfilter
@register.filter
def replace(value, arg):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if len(arg.split('|')) != 2:
        return value

    what, to = arg.split('|')
    return value.replace(what, to)
