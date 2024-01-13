from django import template
from django.contrib.auth.models import Group 

register = template.Library()

@register.filter(name='has_group')
def has_group(user, buyer): 
    group = Group.objects.get(name=buyer) 
    return True if group in user.groups.all() else False