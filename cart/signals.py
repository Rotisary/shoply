from django.db.models.signals import post_save
from django.contrib.auth import user_logged_in, user_logged_out
from notifications.signals import notify
from django.dispatch import receiver
# from django.utils.translation import ugettext_lazy as _
from .models import Order

# @receiver(post_save, sender=Order)
# def order_was_made(instance, user, **kwargs):
#         notify.send(actor=user, recipient=user,  verb="You have an order to attend to")

# post_save.connect(order_was_made, sender=Order)

# @receiver(user_logged_in)
# def user_signed_in(sender, user, **kwargs):
#     notify.send(user, recipient=user, verb='you signed in')


# @receiver(user_logged_out)
# def user_signed_out(sender, user, **kwargs):
#     notify.send(user, recipient=user, verb='you signed out')


