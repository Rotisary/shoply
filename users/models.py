from django.db import models
from django.contrib.auth.models import AbstractUser
from products.models import Product
from django.conf import settings

class CustomUser(AbstractUser):
    BUYER = 'BY'
    SELLER = 'SL'
    USER_CHOICE = [
        (BUYER, 'buyer'),
        (SELLER, 'seller'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_CHOICE, default=BUYER)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile',on_delete=models.CASCADE)
    wishlist = models.ManyToManyField(Product, related_name='wishlists_in', blank=True)
    favourite = models.ManyToManyField("self", related_name='favourites_in', symmetrical=False, blank=True)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='created_at', blank=True, null=True)


    def __str__(self):
        return f"{self.user.username}'s profile"


class Dashboard(models.Model):
    dashboard_user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='dashboard', on_delete=models.CASCADE, null=True)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='created_at', blank=True, null=True)


    def __str__(self):
        return f"{self.dashboard_user.username}'s Dashboard"
