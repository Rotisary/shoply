from django.db import models
from django.conf import settings
from users.models import Profile
from products.models import Product


class CartItems(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', related_name='cart', on_delete=models.CASCADE, blank=True)
    item = models.ForeignKey(Product, related_name='item_product', on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='item_seller', null=True)


    def cart_item_price(self):
        return self.quantity * self.item.price


    def __str__(self):
        return f"{self.user.username}'s cart item,  cart item {self.id}"


class Cart(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItems, related_name='cart_products', blank=True)
    ordered = models.BooleanField(default=False)

    
    def no_of_items(self):
        return self.items.count()

    
    def cart_price(self):
        total = 0.00
        for cart_item in self.items.all():
            total += cart_item.cart_item_price()
        return total 



    def __str__(self):
        return f"{self.profile.user.username}'s Cart"


class Order(models.Model):
    PALMPAY = 'PY'
    OPAY = 'OP'
    MONIEPOINT = 'MP'
    UNITED_BANK_OF_AFRICA = 'UBA'
    FIRST_BANK_OF_NIGERIA = 'FBN'
    GUARANTEE_TRUST_BANK = 'GTB'
    PAYMENT_CHOICES = [
        (PALMPAY, 'Palmpay'),
        (OPAY, 'Opay'),
        (MONIEPOINT, 'Moniepoint'),
        (UNITED_BANK_OF_AFRICA, 'UBA'),
        (FIRST_BANK_OF_NIGERIA, 'First Bank'),
        (GUARANTEE_TRUST_BANK, 'GTB')
    ]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING) 
    delivery_address = models.CharField(blank=True, null=True)
    payment_option = models.CharField(choices=PAYMENT_CHOICES, default=PALMPAY, null=True, blank=True)
    attended_to = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.owner.username}'s order, order {self.id}"