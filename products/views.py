from django.shortcuts import render
from .models import Product


def products_list(request):
    products = Product.objects.all()
    context = {'products': products } 
    return render(request, 'products/products.html', context)


def electronics_list(request):
    products = Product.objects.filter(category='EL')
    context = {'products': products } 
    return render(request, 'products/electronics.html', context)


def arts_list(request):
    products = Product.objects.filter(category='AR')
    context = {'products': products } 
    return render(request, 'products/arts.html', context)


def beauty_list(request):
    products = Product.objects.filter(category='BE')
    context = {'products': products } 
    return render(request, 'products/beauty.html', context)


def clothings_list(request):
    products = Product.objects.filter(category='CL')
    context = {'products': products } 
    return render(request, 'products/clothings.html', context)


def accessories_list(request):
    products = Product.objects.filter(category='AC')
    context = {'products': products } 
    return render(request, 'products/accessories.html', context)


def toys_list(request):
    products = Product.objects.filter(category='TY')
    context = {'products': products } 
    return render(request, 'products/toys.html', context)


def sports_list(request):
    products = Product.objects.filter(category='SP')
    context = {'products': products } 
    return render(request, 'products/sports.html', context)


def home_products_list(request):
    products = Product.objects.filter(category='HP')
    context = {'products': products } 
    return render(request, 'products/home_products.html', context)