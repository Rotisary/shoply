from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from .decorators import allowed_users, login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.urls import reverse
from products.models import Product
from .forms import UserRegisterForm
from .models import Profile, Dashboard
from cart.models import CartItem
from products.custom_functions import get_cart_products


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid:
            form.save()
            name = form.cleaned_data.get('username')
            messages.success(request, f"account has been created for {name}")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required()
@allowed_users(allowed_roles=['seller'])
def dashboard_view(request, username):
    try:
        dashboard = Dashboard.objects.get(dashboard_user__username=username)
    except Dashboard.DoesNotExist:
        dashboard = Dashboard.objects.create(dashboard_user=request.user)
    
    context = {'dashboard': dashboard}
    return render (request, 'users/dashboard.html', context)


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        # check if user exists
        if user is not None:
            login(request, user)
            return redirect('products')
 
    context = {}
    return render(request, 'users/login.html', context)


def LogoutPage(request):
    logout(request)
    return redirect('login')


@login_required()
def add_to_wishlist(request, pk):
    if request.method == "POST":
        try:
            product = Product.listed.get(id=pk)
            user = request.user.profile
            if user == product.seller.profile:
                messages.info(request, 'you cannot your own products to wishlist')
            elif user.wishlist.filter(id=product.id).first():
                user.wishlist.remove(product)
                messages.success(request, f'product has been removed from wishlist')
            else:
                user.wishlist.add(product)
                messages.success(request, f'product has been successfully added to wishlist')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('400 error: failed to add product to wishlist')
    else:
        return redirect('products')


@login_required()
def wishlist_view(request, username):
    wishlist_products = request.user.profile.wishlist.all()
    if wishlist_products.exists():

        # call get_cart_products function
        cart_items = CartItem.objects.select_related('item').filter(user=request.user, cart=request.user.profile.cart)
        if cart_items.exists():
            list = get_cart_products(cart_items)
        else:
            list = []

        # paginate queryset
        paginator = Paginator(wishlist_products, 4)

        num_of_pages = paginator.num_pages
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
            "num_of_pages": num_of_pages,
            "products_list": list
        } 
    else:
        messages.info(request, 'your wishlist is empty. Add products to your wishlist so that you can easily find them later')
        context = {}
    return render (request, 'users/wishlist.html', context)


@login_required()
def add_to_favourites(request, username):
    try:
        user_to_add = Profile.objects.get(user__username=username)
        current_user_profile = request.user.profile
        if current_user_profile == user_to_add:
            messages.info(request, 'you cannot add yourself to your favourites list')
        elif current_user_profile.favourite.filter(user__username=user_to_add.user.username).first():
            current_user_profile.favourite.remove(user_to_add)
            messages.success(request, f'seller has been removed from favourites')
        else:
            current_user_profile.favourite.add(user_to_add)
            messages.success(request, f'seller has been successfully added to favourites')
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('failed to add seller to favourites')


@login_required()
def favourites_view(request, username):
    favourite_sellers = request.user.profile.favourite.all()
    if favourite_sellers.exists():
        paginator = Paginator(favourite_sellers, 10)

        num_of_pages = paginator.num_pages
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
            "num_of_pages": num_of_pages
        } 
    else:
        messages.info(request, "you don't have any favourite sellers yet")
        context = {}
    return render (request, 'users/favourites.html', context)