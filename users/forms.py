from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm 
from users.models import CustomUser


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email',  'password1', 'password2','user_type']