from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from products.models import Product
from users.models import CustomUser, Profile, Dashboard
from .models import Cart, Order, CartItems
from .forms import OrderCreationForm
from django.contrib import messages
from django.core.mail import send_mail
from shoply.settings import EMAIL_HOST_USER
from django.conf import settings
from users.decorators import allowed_users


def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    current_user = request.user
    cart_item, created = CartItems.objects.get_or_create(user=current_user, 
                                                        cart=current_user.profile.cart,
                                                        item=product,
                                                        seller=product.seller)
    if current_user.profile.cart.items.filter(id=cart_item.id).first():
        current_user.profile.cart.items.remove(cart_item)
    else:
        current_user.profile.cart.items.add(cart_item)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_products_list(request, username):
    cart = request.user.profile.cart
    product = request.user.profile.cart.items.all()
    context = {
        'cart': cart,
        'product': product
    }
    return render(request, 'cart/cart.html', context)


def increase_item_quantity(request, pk):
    cart_item = CartItems.objects.filter(id=pk).first()
    if cart_item.quantity >= 1:
        cart_item.quantity += 1
        cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def decrease_item_quantity(request, pk):
    cart_item = CartItems.objects.filter(id=pk).first()
    if cart_item.quantity >= 1:
        cart_item.quantity -= 1
        cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def checkout_view(request, pk):
    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid:
            order = form.save(commit=False)
            order.owner = request.user
            order.cart = request.user.profile.cart
            order.save()


            subject = "New Order"
            message =  "you have a new order to attend to"
            cart_item = order.cart.items.all()
            def sendmail(cart_item):
                recipients = []

                for item in cart_item:
                    email = item.seller.email
                    recipients_email = email
                    recipients.append(recipients_email)

                return recipients
            
            recipient_list = sendmail(cart_item)
            send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=False)
        return redirect('order-confirmed')
    else:
        form = OrderCreationForm()


    cart = request.user.profile.cart
    cart_item = request.user.profile.cart.items.all()
    context = {
            'form': form,
            'cart': cart,
            'cart_item': cart_item
        }
    return render(request, 'cart/checkout.html', context)


@allowed_users(allowed_roles=['seller'])
def order_list_view(request, username):
    orders = Order.objects.filter(cart__items__item__seller=request.user.id)
    context = {'orders': orders }
    return render(request, 'cart/orders.html', context)


@allowed_users(allowed_roles=['seller'])
def order_detail_view(request, pk):
    order =  Order.objects.get(id=pk)
    items = order.cart.items.filter(item__seller=request.user)
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'cart/order_detail.html', context)


def attended_to_view(request, pk):
    order = Order.objects.filter(id=pk).first()
    if order.attended_to == False:
        order.attended_to = True
        order.save()
    elif order.attended_to == True:
        order.attended_to = False  
        order.save()
    elif order.attended_to == False:
        order_cart_items = order.cart.items.all()
        for cart_item in order_cart_items:
            order.cart.items.remove(cart_item)
        order.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def order_confirmation_view(request):
    return render(request, 'cart/order-confirmation.html')