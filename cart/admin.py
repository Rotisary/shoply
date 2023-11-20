from django.contrib import admin

from .models import Cart, Order, CartItems

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(CartItems)
