from django import template

register = template.Library()


@register.filter
def odd(num):
    return num % 2
