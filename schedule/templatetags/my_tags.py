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


@register.filter
def convertdays(day):
    try:
        output = ""
        if day == "mo":
            output = "Monday"
        elif day == "tu":
            output = "Tuesday"
        elif day == "we":
            output = "Wednesday"
        elif day == "th":
            output = "Thursday"
        elif day == "fr":
            output = "Friday"
        elif day == "sa":
            output = "Saturday"
        elif day == "su":
            output = "Sunday"
        return output
    except (ValueError, ZeroDivisionError):
        return None
