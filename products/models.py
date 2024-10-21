from django.db import models
from django.conf import settings
from django.urls import reverse


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_listed=True)


class Product(models.Model):
    ELECTRONICS = "EL"
    ARTS = "AR"
    BEAUTY = "BE"
    CLOTHINGS = "CL"
    ACCESSORIES = "AC"
    TOYS = "TY"
    SPORTS = "SP"
    HOME_PRODUCTS = "HP"
    CATEGORY_CHOICES = [
        (ELECTRONICS, 'Electronics'),
        (ARTS, 'Arts&Crafts'),
        (BEAUTY, 'Beauty'),
        (CLOTHINGS, 'Clothings'),
        (ACCESSORIES, 'Accessories'),
        (TOYS, 'Toys&Games'),
        (SPORTS, 'Sports&Outdoor'),
        (HOME_PRODUCTS, 'Home Products'),
    ]
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products', on_delete=models.CASCADE)
    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES, default=ELECTRONICS)
    name = models.CharField(max_length=100)
    image = models.ImageField(default='product_default.png')
    price = models.FloatField()
    description = models.TextField(max_length=300, blank=True)
    stock = models.IntegerField()
    ordered_count = models.IntegerField(default=0)
    is_listed = models.BooleanField(default=False)
    time_added = models.DateTimeField(auto_now_add=True, verbose_name='created_at', blank=True, null=True)

    objects = models.Manager()
    listed = ProductManager()

    def __str__(self):
        return f"{self.name}"

    
    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(blank=False)
    time_written = models.DateTimeField(auto_now_add=True, verbose_name='created_at', blank=True, null=True)

    
    def __str__(self):
        return f"{self.product.name}'s review, review  No: {self.id}"


class Reply(models.Model):
    review = models.ForeignKey(Review, related_name='replies', on_delete=models.CASCADE)
    replier = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='replies', on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    time_written = models.DateTimeField(auto_now_add=True, verbose_name='created_at', blank=True, null=True)


    def __str__(self):
        return f"{self.review.id}'s reply, reply No: {self.id}"

    


    