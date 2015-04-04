from django import template

register = template.Library()


@register.filter
def key_value(dictionary, key):
    return dictionary[key]
