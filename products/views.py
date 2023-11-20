from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .models import Product, Review, Reply
from .forms import ReviewForm, ReplyForm
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from users.decorators import allowed_users
from django.urls import reverse


@allowed_users(allowed_roles=['seller'])
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
    context = {
        'products': products
     } 
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

@method_decorator(allowed_users(allowed_roles=['seller']), name="dispatch")
class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'category', 'price', 'stock', 'image']

    
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'

@method_decorator(allowed_users(allowed_roles=['seller']), name="dispatch")
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

@method_decorator(allowed_users(allowed_roles=['seller']), name="dispatch")
class ProductDeleteView(UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'


    def test_func(self):
        product = self.get_object()
        if self.request.user == product.seller:
            return True
        else:
            return False


def ProductReviewView(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.writer = request.user
            review.save()
            # return reverse('reviews',  review.product.id)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'product': product,
    }
    return render (request, 'products/create-reviews.html', context)


def ReviewListView(request, pk):
    product = Product.objects.filter(id=pk).first()
    reviews = Review.objects.filter(product=pk)
    context = {
        'reviews': reviews,
        'product': product
    }
    return render(request, 'products/reviews-list.html', context)
        

def ReviewReplyView(request, pk):
    review = get_object_or_404(Review, id=pk)
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.review = review
            reply.replier = request.user
            reply.save()
            # return reverse ('reviews', {'pk': pk})
    else:
        form = ReplyForm()
    
    context = {
        'form': form,
        'review': review,
    }
    return render (request, 'products/create-replies.html', context)


def ReplyListView(request, pk):
    review = Review.objects.filter(id=pk).first()
    replies = Reply.objects.filter(review=pk)
    context = {
        'replies': replies,
        'review': review
    }
    return render(request, 'products/replies-list.html', context)


class ReviewDeleteView(UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'products/review-delete-confirm.html'
    
    def get_success_url(self):
        review = self.get_object()
        return reverse('reviews', kwargs={'pk': review.product.id})

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.writer:
            return True
        else:
            return False


class ReplyDeleteView(UserPassesTestMixin, DeleteView):
    model = Reply
    template_name = 'products/reply-delete-confirm.html'
    
    def get_success_url(self):
        reply = self.get_object()
        return reverse('replies', kwargs={'pk': reply.review.id})

    def test_func(self):
        reply = self.get_object()
        if self.request.user == reply.replier:
            return True
        else:
            return False


