from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from products.models import Product
from .models import Cart, Order, CartItem, OrderItem
from .forms import OrderCreationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from shoply.settings import EMAIL_HOST_USER
from django.conf import settings
from users.decorators import allowed_users, login_required


@login_required()
def add_to_cart(request, pk):
    current_user = request.user
    try:
        product = Product.listed.select_related('seller').get(id=pk)
        if current_user == product.seller:  
            return  HttpResponseForbidden('error 403: you are not allowed to perform this action')
        else: 
            if product.stock <= 0: 
                return HttpResponseBadRequest('error 400: you cannot add this product to cart, it is out of stock') 
            else:  
                cart_item = CartItem.objects.create(user=current_user, 
                                                    cart=current_user.profile.cart,
                                                    item=product,
                                                    category=product.category,
                                                    seller=product.seller) 
                
                cart_item.save()
                current_user.profile.cart.items.add(cart_item) 
                messages.success(request, 'product has been successfully added to cart')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Product.DoesNotExist:
        return HttpResponseNotFound('ERROR 404: could not add product to cart, it has been unlisted')


def remove_from_cart(request, pk):
    current_user = request.user
    try:
        cart_item = CartItem.objects.get(id=pk)
        if current_user.profile.cart.items.filter(id=cart_item.id):
            current_user.profile.cart.items.remove(cart_item) 
            messages.success(request, 'product has been removed from cart')
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except CartItem.DoesNotExist:
        return HttpResponseNotFound('ERROR 404: this product has been unlisted')


@login_required()
def cart_products_list(request, username):
    try:
        cart = request.user.profile.cart
        products = cart.items.all().order_by('-time_created')
        if products.exists():
            paginator = Paginator(products, 4)

            num_of_pages = paginator.num_pages
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            context = {
                "cart": cart,
                "page_obj": page_obj,    
                "num_of_pages": num_of_pages
             }    
        else:
            messages.info(request, 'your cart is empty. Go to the products page to add products to your cart')
            context = {
                "cart": cart
             }
    except Cart.DoesNotExist:
        cart = Cart.objects.create(profile=request.user.profile)

    return render(request, 'cart/cart.html', context)


@login_required()
def increase_item_quantity(request, pk):
    try:
        cart_item = CartItem.objects.get(id=pk, item__is_listed=True)
        if cart_item.quantity >= 1:
            cart_item.quantity += 1
            cart_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except CartItem.DoesNotExist:
        HttpResponseNotFound('this product has been unlisted')


@login_required()
def decrease_item_quantity(request, pk):
    try:
        cart_item = CartItem.objects.get(id=pk, item__is_listed=True)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except CartItem.DoesNotExist:
        HttpResponseNotFound('this product has been unlisted')


@login_required()
def checkout_view(request, username):
    if request.method == 'POST':
        cart_items = request.user.profile.cart.items.all()
        if cart_items.exists():
            form = OrderCreationForm(request.POST)
            if form.is_valid:
                order = form.save(commit=False)
                order.owner = request.user
                order.save()


                def create_order_items(product_list):
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


                create_order_items(cart_items)
                request.user.profile.cart.items.clear()
                CartItem.objects.filter(user=request.user, cart=request.user.profile.cart).delete()
                     
                        
                def send_mail_func(items):
                    recipients = []
                    for item in items:
                        email = item.seller.email
                        recipients_email = email
                        recipients.append(recipients_email)
                    return recipients


                subject = "New Order"
                message =  "you have a new order to attend to"
                order_items = order.order_items.all()
                recipient_list = send_mail_func(order_items)
                send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=False)
        else:
            messages.error(request, "bad request")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        if request.user.profile.cart.items.all().exists():
            form = OrderCreationForm()
        else:
            messages.info(request, 'please add products to your cart')
            return HttpResponseRedirect(reverse_lazy('cart', kwargs={'username': request.user.username}))


    cart = request.user.profile.cart
    cart_items = request.user.profile.cart.items.all()
    context = {
            'form': form,
            'cart': cart,
            'cart_items': cart_items
        }
    return render(request, 'cart/checkout.html', context)



@login_required()
@allowed_users(allowed_roles=['seller'])
def order_list_view(request, username):
    orders = Order.objects.filter(order_items__seller=request.user).order_by('-time_of_order').distinct()
    if orders.exists():
        paginator = Paginator(orders, 10)

        num_of_pages = paginator.num_pages
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
            "num_of_pages": num_of_pages
        }
    else:
        messages.info(request, 'you do not have any orders yet')
        context = {}

    return render(request, 'cart/orders.html', context)


@login_required()
@allowed_users(allowed_roles=['seller'])
def order_detail_view(request, pk):
    try:
        order =  Order.objects.prefetch_related('order_items').get(id=pk)
        items = order.order_items.filter(seller=request.user)
        if items.exists():
            def total_order_price(order_items):
                Total_Price = 0.00
                for item in order_items:
                    Total_Price += item.order_item_price()
                return Total_Price
        else:
            HttpResponseBadRequest('ERROR 400: this order is empty')
        
    except Order.DoesNotExist:
        return HttpResponseNotFound('ERROR 404: this order has been deleted')
    
    context = {
        'order': order,
        'items': items,
        'Total_Price': total_order_price(items),
     }   
    return render(request, 'cart/order_detail.html', context)


@login_required()
def attended_to_view(request, pk):
    try:
        order = Order.objects.get(id=pk)
        if order.attended_to == False:
            order.attended_to = True
            order.save()
        elif order.attended_to == True:
            order.attended_to = False  
            order.save()
    except Order.DoesNotExist:
        return HttpResponseNotFound('ERROR 404: this order has been deleted')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))