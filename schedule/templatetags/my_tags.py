from django import template

register = template.Library()


@register.filter
def modulo(num, val):
    try:
        outputs = num % val
        return str(outputs).zfill(2)
    except (ValueError, ZeroDivisionError):
        return None


@register.filter
def divide(value, arg):
    try:
        outputs = int(int(value) / int(arg))
        return str(outputs).zfill(2)
    except (ValueError, ZeroDivisionError):
        return None
