from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404, get_list_or_404
from .models import Product, Review, Reply
from cart.models import CartItem, Cart
from .forms import ReviewForm, ReplyForm
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin 
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.contrib import messages
from users.decorators import allowed_users, login_required
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from .custom_functions import get_cart_products


@login_required()
@allowed_users(allowed_roles=['seller'])
def inventory_list(request):
    products = Product.objects.filter(seller=request.user)
    if products.exists():

        # paginate the queryset
        paginator = Paginator(products, 4)

        num_of_pages = paginator.num_pages
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj,
            "num_of_pages": num_of_pages
         }       
    else:
        messages.info(request, "you don't have any products in your inventory")
        context = {}
    return render(request, 'products/inventory.html', context)  



@login_required()
@allowed_users(allowed_roles=['seller'])
def listing(request, pk):
    try:
        product = Product.objects.get(id=pk)
        if product.is_listed == False:
            product.is_listed = True
            product.save()
            messages.success(request, f'your product has been listed')
        elif product.is_listed == True:
            product.is_listed = False
            product.save()
            messages.success(request, f'your product has been unlisted')
    except Product.DoesNotExist:
        return HttpResponseNotFound('ERROR 404: product does not exist')


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def products_list(request):
    products = Product.listed.all().order_by('-time_added')
    if products.exists():

        # call get_cart_products function
        if request.user.is_authenticated:
            cart_items = CartItem.objects.select_related('item').filter(user=request.user)
            if cart_items.exists():
                list = get_cart_products(cart_items)
            else:
                list = []
        else:
            list = []

        # paginate the queryset
        paginator = Paginator(products, 4)

        num_of_pages = paginator.num_pages
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj,
            "num_of_pages": num_of_pages,
            'products_list': list
        }       
    else:
        messages.info(request, "There are no listed products yet, please try again later")
        context = {}
    return render(request, 'products/products.html', context)


def electronics_list(request):
    products = Product.listed.filter(category='EL').order_by('-time_added')
    if products.exists():

        # call get_cart_products function
        if request.user.is_authenticated:
            cart_items = CartItem.objects.select_related('item').filter(user=request.user)
            if cart_items.exists():
                list = get_cart_products(cart_items)
            else:
                list = []
        else:
            list = []

        # paginate the queryset
        paginator = Paginator(products, 4)

        num_of_pages = paginator.num_pages
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj,
            "num_of_pages": num_of_pages,
            "products_list": list
         }       
    else:
        messages.info(request, 'there are no listed products in this category, please try again later')
        context = {}
    return render(request, 'products/electronics.html', context)


def arts_list(request):
    products = Product.listed.filter(category='AR').order_by('-time_added')
    if products.exists():

        # call get_cart_products function
        if request.user.is_authenticated:
            cart_items = CartItem.objects.select_related('item').filter(user=request.user)
            if cart_items.exists():
                list = get_cart_products(cart_items)
            else:
                list = []
        else:
            list = []

        # paginate the queryset
        paginator = Paginator(products, 4)

        num_of_pages = paginator.num_pages
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj,
            "num_of_pages": num_of_pages,
            "products_list": list
         }       
    else:
        messages.info(request, 'there are no listed products in this category, please try again later')
        context = {}
    return render(request, 'products/arts.html', context)


def beauty_list(request):
    products = Product.listed.filter(category='BE').order_by('-time_added')
    if products.exists():

        # call get_cart_products function
        if request.user.is_authenticated:
            cart_items = CartItem.objects.select_related('item').filter(user=request.user)
            if cart_items.exists():
                list = get_cart_products(cart_items)
            else:
                list = []
        else:
            list = []

        # paginate the queryset
        paginator = Paginator(products, 4)

        num_of_pages = paginator.num_pages
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj,
            "num_of_pages": num_of_pages,
            "products_list": list
         }       
    else:
        messages.info(request, 'there are no listed products in this category, please try again later')
        context = {}
    return render(request, 'products/beauty.html', context)


def clothings_list(request):
    products = Product.listed.filter(category='CL').order_by('-time_added')
    if products.exists():

        # call get_cart_products function
        if request.user.is_authenticated:
            cart_items = CartItem.objects.select_related('item').filter(user=request.user)
            if cart_items.exists():
                list = get_cart_products(cart_items)
            else:
                list = []
        else:
            list = []

        # paginate the queryset
        paginator = Paginator(products, 4)

        num_of_pages = paginator.num_pages
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj,
            "num_of_pages": num_of_pages,
            "products_list": list
         }       
    else:
        messages.info(request, 'there are no listed products in this category, please try again later')
        context = {}
    return render(request, 'products/clothings.html', context)


def accessories_list(request):
    products = Product.listed.filter(category='AC').order_by('-time_added')
    if products.exists():

        # call get_cart_products function
        if request.user.is_authenticated:
            cart_items = CartItem.objects.select_related('item').filter(user=request.user)
            if cart_items.exists():
                list = get_cart_products(cart_items)
            else:
                list = []
        else:
            list = []

        # paginate the queryset
        paginator = Paginator(products, 4)

        num_of_pages = paginator.num_pages
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj,
            "num_of_pages": num_of_pages,
            "products_list": list
         }       
    else:
        messages.info(request, 'there are no listed products in this category, please try again later')
        context = {}
    return render(request, 'products/accessories.html', context)


def toys_list(request):
    products = Product.listed.filter(category='TY').order_by('-time_added')
    if products.exists():

        # call get_cart_products function
        if request.user.is_authenticated:
            cart_items = CartItem.objects.select_related('item').filter(user=request.user)
            if cart_items.exists():
                list = get_cart_products(cart_items)
            else:
                list = []
        else:
            list = []

        # paginate the queryset
        paginator = Paginator(products, 4)

        num_of_pages = paginator.num_pages
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj,
            "num_of_pages": num_of_pages,
            "producs_list": list
         }       
    else:
        messages.info(request, 'there are no listed products in this category, please try again later')
        context = {}
    return render(request, 'products/toys.html', context)


def sports_list(request):
    products = Product.listed.filter(category='SP').order_by('-time_added')
    if products.exists():

        # call get_cart_products function
        if request.user.is_authenticated:
            cart_items = CartItem.objects.select_related('item').filter(user=request.user)
            if cart_items.exists():
                list = get_cart_products(cart_items)
            else:
                list = []
        else:
            list = []

        # paginate the queryset
        paginator = Paginator(products, 4)

        num_of_pages = paginator.num_pages
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj,
            "num_of_pages": num_of_pages,
            "products_list": list
         }       
    else:
        messages.info(request, 'there are no listed products in this category, please try again later')
        context = {}
    return render(request, 'products/sports.html', context)


def home_products_list(request):
    products = Product.listed.filter(category='HP').order_by('-time_added')
    if products.exists():

        # call get_cart_products function
        if request.user.is_authenticated:
            cart_items = CartItem.objects.select_related('item').filter(user=request.user)
            if cart_items.exists():
                list = get_cart_products(cart_items)
            else:
                list = []
        else:
            list = []

        # paginate the queryset
        paginator = Paginator(products, 4)

        num_of_pages = paginator.num_pages
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj,
            "num_of_pages": num_of_pages,
            "products_list": list
         }       
    else:
        messages.info(request, 'there are no listed products in this category, please try again later')
        context = {}
    return render(request, 'products/home_products.html', context)


@method_decorator([login_required(), allowed_users(allowed_roles=['seller'])], name="dispatch")
class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'category', 'price', 'description', 'stock', 'image']

    
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'


@method_decorator([login_required(), allowed_users(allowed_roles=['seller'])], name="dispatch")
class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['name', 'category','description', 'price', 'stock', 'image']


    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


    def test_func(self):
        product = self.get_object()
        if self.request.user == product.seller:
            return True
        else:
            return False


@method_decorator([login_required(), allowed_users(allowed_roles=['seller'])], name="dispatch")
class ProductDeleteView(UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'


    def test_func(self):
        product = self.get_object()
        if self.request.user == product.seller:
            return True
        else:
            return False


@login_required()
def product_review(request, pk):
    # get current user
    current_user = request.user

    try:
        product = Product.listed.select_related('seller').get(id=pk)
        if current_user == product.seller:  
            return HttpResponseForbidden('error 403: you are not allowed to perform this action')
        else:  
            if request.method == "POST":
                form = ReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.product = product
                    review.writer = request.user
                    review.save()
                    messages.success(request, f'your review has been added')
                    return HttpResponseRedirect(reverse_lazy('reviews',  kwargs= {'pk': review.product.id}))
            else:
                form = ReviewForm()
    except Product.DoesNotExist:
        return HttpResponseNotFound('ERROR 404: this product has been deleted')
    
    context = {
        'form': form,
        'product': product,
    }
    return render (request, 'products/create-reviews.html', context)


def review_list(request, pk):
    product = Product.listed.prefetch_related('reviews').get(id=pk)
    reviews = product.reviews.all().order_by('-time_written')
    if reviews.exists():

        # paginate the queryset
        paginator = Paginator(reviews, 4)

        num_of_pages = paginator.num_pages
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
            "num_of_pages": num_of_pages,
            'product': product
         } 
    else:
        messages.info(request, "this product has no reviews")
        context = { 
            "product": product
         }
    return render(request, 'products/reviews-list.html', context)
        

@login_required()
def reply(request, pk):
    try:
        review = Review.objects.get(id=pk)
        if request.method == "POST":
            form = ReplyForm(request.POST)
            if form.is_valid():
                reply = form.save(commit=False)
                reply.review = review
                reply.replier = request.user
                reply.save()
                messages.success(request, f'your reply has been added')
                return HttpResponseRedirect(reverse ('replies', kwargs= {'pk': reply.review.id}))
        else:
            form = ReplyForm()
    except Product.DoesNotExist:
        return HttpResponseNotFound('ERROR 404: this review has been deleted')
        
    context = {
        'form': form,
        'review': review,
    }
    
    return render (request, 'products/create-replies.html', context)


def reply_list(request, pk):
    review = Review.objects.prefetch_related('replies').get(id=pk)
    replies = review.replies.all().order_by('-time_written')
    if replies.exists():

        # paginate the queryset
        paginator = Paginator(replies, 4)

        num_of_pages = paginator.num_pages
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
            "num_of_pages": num_of_pages,
            'review': review
        }
    else:
        messages.info(request, "this review has no replies")
        context = { 
            "review": review
         }
    return render(request, 'products/replies-list.html', context)


@method_decorator(login_required(), name="dispatch")
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


@method_decorator(login_required(), name="dispatch")
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


def search_view(request):
        # get searched term
        search = request.GET.get('search')

        if search == " ":
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            searched = Product.listed.filter( 
                Q(name__icontains=search) | Q(category__icontains=search) | Q(description__icontains=search)
                ).order_by('-ordered_count')
            if searched.exists():

                # call get_cart_products function
                cart_items = CartItem.objects.select_related('item').filter(
                    user=request.user, 
                    cart=request.user.profile.cart
                    )
                if cart_items.exists():
                    list = get_cart_products(cart_items)
                else:
                    list = []

                # paginate the queryset
                paginator = Paginator(searched, 4)

                num_of_pages = paginator.num_pages
                page_number = request.GET.get("page")
                page_obj = paginator.get_page(page_number)

                context = {
                    "page_obj": page_obj,
                    "num_of_pages": num_of_pages,
                    "products_list": list
                } 
            else:
                messages.info(request, "sorry, no product matches your search term")
                context = {}
        return render(request, 'products/search.html', context)


# cart_items = CartItem.objects.filter(user__username='becca')
# if cart_items.exists():
#     products = []
#     for cart_item in cart_items:
#         product = cart_item.item
#         products.append(product)