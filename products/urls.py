from django.urls import path
from products import views
from products.views import (
    ProductCreateView,
    ProductDetailView,
    ProductUpdateView, 
    ProductDeleteView, 
    ReviewDeleteView,
    ReplyDeleteView
)


urlpatterns = [
    # product category list urlpatterns
    path('', views.products_list, name='products'),
    path('inventory/', views.inventory_list, name='inventory'),
    path('list/<int:pk>/', views.listing, name='listing'),
    path('electronics/', views.electronics_list, name='electronics'),
    path('arts/', views.arts_list, name='arts'),
    path('beauty/', views.beauty_list, name='beauty'),
    path('clothings/', views.clothings_list, name='clothings'),
    path('accessories/', views.accessories_list, name='accessories'),
    path('toys/', views.toys_list, name='toys'),
    path('sports/', views.sports_list, name='sports'),
    path('home-products/', views.home_products_list, name='home-products'),

    # product crud operation urlpatterns
    path('create-product/', ProductCreateView.as_view(), name='create'),
    path('product/<int:pk>/detail/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),

    # product review, reply urlpatterns
    path('product/<int:pk>/drop-review/', views.product_review, name='drop-review'),
    path('product/<int:pk>/reviews/', views.review_list, name='reviews'),
    path('review/<int:pk>/reply/', views.reply, name='drop-reply'),
    path('reply/<int:pk>/replies/', views.reply_list, name='replies'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
    path('reply/<int:pk>/delete/', ReplyDeleteView.as_view(), name='reply-delete'),
    
    path('search/', views.search_view, name='search'),
]