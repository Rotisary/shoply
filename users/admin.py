from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, Dashboard

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Profile)
admin.site.register(Dashboard)