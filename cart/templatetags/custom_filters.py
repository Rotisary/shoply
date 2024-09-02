from django import template
from django.utils.timesince import timesince
from datetime import datetime, timedelta
from django.utils import timezone

register = template.Library()

@register.filter
def custom_time_display(value):
    now = datetime.now()
    diff = timezone.make_aware(now) - value

    if diff < timedelta(hours=1):
        return value.strftime("%H:%M")  
    elif diff < timedelta(days=1):
        return f"{timesince(value).split(',')[0]} ago"
    else:
        return value
    
