# E_comm/templatetags/email_extras.py

from django import template
from django.utils.dateformat import format
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def add_days(value, days):
    """
    Add a specified number of days to a date
    Usage: {{ order.shipped_at|add_days:2 }}
    """
    if not value:
        return ''
    
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, "%B %d, %Y")
        except ValueError:
            return value
            
    new_date = value + timedelta(days=int(days))
    return format(new_date, 'F j, Y')