from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from users import views as  user_views
from cart import views as cart_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',  user_views.register, name='register'),
    path('dashboard/<str:username>/', user_views.dashboard_view, name='dashboard'),
    path('login/', user_views.LoginPage, name='login'),
    path('logout/', user_views.LogoutPage, name='logout'),
    path('wishlist/add/<int:pk>/', user_views.add_to_wishlist, name='add-to-wishlist'),
    path('<str:username>/wishlist/', user_views.wishlist_view, name='wishlist'),
    path('favourite/add/<str:username>/', user_views.add_to_favourites, name='add-to-favourites'),
    path('<str:username>/favourites/', user_views.favourites_view, name='favourites'),
    path('cart/add/<int:pk>/', cart_views.add_to_cart, name='add-to-cart'),
    path('<str:username>/cart/', cart_views.cart_products_list, name='cart'),
    path('item/<int:pk>/quantity/increase/', cart_views.increase_item_quantity, name='increase-quantity'),
    path('item/<int:pk>/quantity/decrease/', cart_views.decrease_item_quantity, name='decrease-quantity'),
    path('order/', cart_views.create_order, name='order'),
    path('<str:username>/orders/', cart_views.order_list_view, name='order-list'),
    path('order/<int:pk>/detail/', cart_views.order_detail_view, name='order-detail'),
    path('cart/<int:pk>/checkout/', cart_views.checkout_view, name='checkout'),
    path('order-confirmed/', cart_views.order_confirmation_view, name='order-confirmed'),
    path('order/<int:pk>/attended_to/', cart_views.attended_to_view, name='attended-to'),
    path('', include('products.urls')),
    path('inbox/notifications/', include('notifications.urls', namespace='notifications'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)