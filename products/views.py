from django.shortcuts import render, HttpResponseRedirect
from .models import Product
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.conf import settings

user = settings.AUTH_USER_MODEL
def inventory_list(request):
    products = Product.objects.filter(seller=request.user)
    context = {'products': products } 
    return render(request, 'products/inventory.html', context)


def listing(request, pk):
    product = Product.objects.get(id=pk)
    if product.listed == False:
        product.listed = True
        product.save()
    elif product.listed == True:
        product.listed = False
        product.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def products_list(request):
    products = Product.objects.filter(listed=True)
    context = {'products': products } 
    return render(request, 'products/products.html', context)


def electronics_list(request):
    products = Product.objects.filter(category='EL', listed=True)
    context = {'products': products } 
    return render(request, 'products/electronics.html', context)


def arts_list(request):
    products = Product.objects.filter(category='AR', listed=True)
    context = {'products': products } 
    return render(request, 'products/arts.html', context)


def beauty_list(request):
    products = Product.objects.filter(category='BE', listed=True)
    context = {'products': products } 
    return render(request, 'products/beauty.html', context)


def clothings_list(request):
    products = Product.objects.filter(category='CL', listed=True)
    context = {'products': products } 
    return render(request, 'products/clothings.html', context)


def accessories_list(request):
    products = Product.objects.filter(category='AC', listed=True)
    context = {'products': products } 
    return render(request, 'products/accessories.html', context)


def toys_list(request):
    products = Product.objects.filter(category='TY', listed=True)
    context = {'products': products } 
    return render(request, 'products/toys.html', context)


def sports_list(request):
    products = Product.objects.filter(category='SP', listed=True)
    context = {'products': products } 
    return render(request, 'products/sports.html', context)


def home_products_list(request):
    products = Product.objects.filter(category='HP', listed=True)
    context = {'products': products } 
    return render(request, 'products/home_products.html', context)


class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'category', 'price', 'stock', 'image']

    
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['name', 'category', 'price', 'stock', 'image']

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


    def test_func(self):
        product = self.get_object()
        if self.request.user == product.seller:
            return True
        else:
            return False


class ProductDeleteView(UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'


    def test_func(self):
        product = self.get_object()
        if self.request.user == product.seller:
            return True
        else:
            return False