from django import template

register = template.Library()

@register.filter(name='is_eq')
def is_eq(value, arg):
    """
    Returns True if value == arg, else False.
    Usage: {% if val|is_eq:other_val %}
    """
    return str(value) == str(arg)
