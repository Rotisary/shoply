from django.contrib.auth.models import Group
from products.models import Product
from django.http import HttpResponse
from django.conf import settings


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists:
                group = request.user.groups.all().first().name


            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator
