from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from products.models import Product
from users.models import Profile, Dashboard
from .models import Cart, Order, CartItems
from .forms import OrderCreationForm
from django.contrib import messages

def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    current_user = request.user
    cart_item, created = CartItems.objects.get_or_create(user=current_user, 
                                                        cart=current_user.profile.cart,
                                                        item=product)
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


def create_order(request):
    if request.method == 'POST':
        order = Order.objects.create(owner=request.user, cart=request.user.profile.cart)
        order.save()
        messages.success(request, f"Your order has been placed")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def order_list_view(request, username):
    orders = Order.objects.filter(cart__items__item__seller=request.user.id)
    context = {'orders': orders }
    return render(request, 'cart/orders.html', context)


def order_detail_view(request, pk):
    order =  Order.objects.get(id=pk)
    items = order.cart.items.filter(item__seller=request.user)
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'cart/order_detail.html', context)


def test(request):
    quantity = request.GET.get('quantity')
    address = request.GET.get('address')
    context = {
        'quantity': quantity,
        'address': address
    }
    return render(request, 'cart/test.html', context)


def checkout_view(request, pk):
    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid:
            order = form.save(commit=False)
            order.owner = request.user
            order.cart = request.user.profile.cart
            order.save()
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


def order_confirmation_view(request):
    return render(request, 'cart/order-confirmation.html')

  

# items = CartItems.objects.all()
# cart = Cart.objects.all()
# items_list = list(items)
# total = 0
# for item in items_list:
#     price = item.cart_item_price() 
#     total += price

# print(total)