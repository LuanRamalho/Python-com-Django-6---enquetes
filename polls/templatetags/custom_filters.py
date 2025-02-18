from django import template

register = template.Library()

@register.filter
def div(value, divisor):
    try:
        return value / divisor
    except (ZeroDivisionError, TypeError):
        return 0
