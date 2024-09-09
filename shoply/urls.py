from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
import debug_toolbar
from django.contrib.auth import views as auth_views
from users import views as  user_views
from cart import views as cart_views


urlpatterns = [
     path('admin/', admin.site.urls),

     # user urlpatterns
     path('register/',  user_views.register, name='register'),
     path('login/', user_views.LoginPage, name='login'),
     path('logout/', user_views.LogoutPage, name='logout'),
     path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), 
         name='password-reset'),
     path('password-reset/done', 
          auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
          name='password_reset_done'),
     path('password-reset-confirm/<uidb64>/<token>/', 
          auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
          name='password_reset_confirm'),
     path('password-reset-complete/', 
          auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_compl.html'), 
          name='password_reset_complete'),

     # dashboard urlpatterns
     path('dashboard/<str:username>/', user_views.dashboard_view, name='dashboard'),
     path('wishlist/add/<int:pk>/', user_views.add_to_wishlist, name='add-to-wishlist'),
     path('<str:username>/wishlist/', user_views.wishlist_view, name='wishlist'),
     path('favourite/add/<str:username>/', user_views.add_to_favourites, name='add-to-favourites'),
     path('<str:username>/favourites/', user_views.favourites_view, name='favourites'),

     # cart operations urlpatterns
     path('cart/add/<int:pk>/', cart_views.add_to_cart, name='add-to-cart'),
     path('<str:username>/cart/', cart_views.cart_products_list, name='cart'),
     path('item/<int:pk>/quantity/increase/', cart_views.increase_item_quantity, name='increase-quantity'),
     path('item/<int:pk>/quantity/decrease/', cart_views.decrease_item_quantity, name='decrease-quantity'),
     path('orders/<str:username>/', cart_views.order_list_view, name='order-list'),
     path('order/<int:pk>/detail/', cart_views.order_detail_view, name='order-detail'),
     path('cart/<str:username>/checkout/', cart_views.checkout_view, name='checkout'),
     # path('order-confirmed/', cart_views.order_confirmation_view, name='order-confirmed'),
     path('order/<int:pk>/attended_to/', cart_views.attended_to_view, name='attended-to'),
     path('', include('products.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
