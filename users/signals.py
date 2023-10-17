from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import UserRegisterForm


@receiver(post_save, sender=User)
def add_to_group(sender, instance, created, **kwargs):
    if created:
            group = Group.objects.get(name='seller')
            instance.groups.add(group)
