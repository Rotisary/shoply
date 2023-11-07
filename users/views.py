from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from products.models import Product
from .forms import UserRegisterForm
from .models import Profile
from django.contrib import messages


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


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('products')
 
    context = {}
    return render(request, 'users/login.html', context)


def LogoutPage(request):
    logout(request)
    return redirect('login')


def add_to_wishlist(request, pk):
    if request.method == "POST":
        product = get_object_or_404(Product, id=pk)
        app_user = request.user.profile
        if app_user.wishlist.filter(id=product.id).first():
            app_user.wishlist.remove(product)
        else:
            app_user.wishlist.add(product)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('products')


def add_to_favourites(request, username):
    user_to_add = Profile.objects.get(user__username=username)
    current_user_profile = request.user.profile
    if current_user_profile.favourite.filter(user__username=user_to_add.user.username).first():
        current_user_profile.favourite.remove(user_to_add)
    else:
        current_user_profile.favourite.add(user_to_add)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))