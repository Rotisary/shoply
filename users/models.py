from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    BUYER = 'BY'
    SELLER = 'SL'
    USER_CHOICE = [
        (BUYER, 'buyer'),
        (SELLER, 'seller'),
    ]
    user_type = models.CharField(choices=USER_CHOICE, default=BUYER)

