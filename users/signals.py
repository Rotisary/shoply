from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from users.models import Profile



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'BY':
            group = Group.objects.get(name='buyer')
            instance.groups.add(group)
        elif instance.user_type == 'SL':
            group = Group.objects.get(name='seller')
            instance.groups.add(group)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender,instance, **kwargs):
    instance.profile.save()