from django.urls import path
from products import views


urlpatterns = [
    path('', views.products_list, name='products'),
    path('electronics/', views.electronics_list, name='electronics'),
    path('arts/', views.arts_list, name='arts'),
    path('beauty/', views.beauty_list, name='beauty'),
    path('clothings/', views.clothings_list, name='clothings'),
    path('accessories/', views.accessories_list, name='accessories'),
    path('toys/', views.toys_list, name='toys'),
    path('sports/', views.sports_list, name='sports'),
    path('home-products', views.home_products_list, name='home-products'),
]