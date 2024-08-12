from django.db import models
from django.conf import settings
from users.models import Profile
from products.models import Product


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', related_name='cart', on_delete=models.CASCADE, blank=True)
    item = models.ForeignKey(Product, related_name='cart_items', on_delete=models.DO_NOTHING, blank=True, null=True)
    category = models.TextField(blank=True)
    quantity = models.IntegerField(default=1)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='item_seller', null=True)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='created_at', blank=True, null=True)


    def cart_item_price(self):
        return self.quantity * self.item.price


    def __str__(self):
        return f"{self.user.username}'s cart item,  cart item {self.id}"


class Cart(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, related_name='cart_products', blank=True)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='created_at', blank=True, null=True)


    
    def no_of_items(self):
        return self.items.count()

    
    def cart_price(self):
        total = 0.00
        for cart_item in self.items.all():
            total += cart_item.cart_item_price()
        return total 



    def __str__(self):
        return f"{self.profile.user.username}'s Cart"


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', related_name='order_items', on_delete=models.CASCADE, blank=True)
    item = models.ForeignKey(Product, related_name='order_items_in', on_delete=models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='order_items_sold', null=True)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='created_at', blank=True, null=True)


    def order_item_price(self):
        return self.quantity * self.item.price


    def __str__(self):
        return f"{self.user.username}'s order item,  order item {self.id}"


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
    delivery_address = models.CharField(blank=True, null=True)
    payment_option = models.CharField(choices=PAYMENT_CHOICES, default=PALMPAY, null=True, blank=True)
    attended_to = models.BooleanField(default=False)
    time_of_order = models.DateTimeField(auto_now_add=True, verbose_name='created_at', blank=True, null=True)


    def __str__(self):
        return f"{self.owner.username}'s order, order {self.id}"