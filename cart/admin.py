from django.contrib import admin

from .models import Cart, Order, CartItem, OrderItem

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(OrderItem)
