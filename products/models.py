from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    image = models.ImageField(default='product_default.png', upload_to='product_pics')
    price = models.FloatField()
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.name}"