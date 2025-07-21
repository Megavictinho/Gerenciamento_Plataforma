from django import template
register = template.Library()
from datetime import date

@register.filter
def get(dict_data, key):
    return dict_data.get(key)

@register.filter
def is_today(value):
    return value == date.today()