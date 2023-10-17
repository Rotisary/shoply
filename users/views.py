from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid:
            form.save()
            name = form.cleaned_data.get('username')
            messages.success(request, f"account has been created for {name}")
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
