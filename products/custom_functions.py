from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from cart.models import OrderItem


# function to get the list of products in each cart item
def get_cart_products(cart_items_qs):
    products = []
    for cart_item in cart_items_qs:
        products.append(cart_item.item)
    return products



# convert each cart item to an order item
def create_order_items(product_list, order, request):
    for cart_item in product_list:
        if cart_item.item.stock < cart_item.quantity:
            messages.error(request, f"could not order product: {cart_item.item.name}, not enough stock available")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
        else:
            order_item = OrderItem.objects.create(user=cart_item.user, 
                                                order=order,
                                                item=cart_item.item,
                                                quantity=cart_item.quantity,
                                                seller=cart_item.seller)
    messages.success(request, f'your order has been placed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



# get the recipients list for django's send mail function    
def send_mail_func(items):
    recipients = []
    for item in items:
        email = item.seller.email
        recipients_email = email
        recipients.append(recipients_email)
    return recipients



# get the total order price specific to each seller (not total cart items price)
def total_order_price(order_items):
    Total_Price = 0.00
    for item in order_items:
        Total_Price += item.order_item_price()
    return Total_Price