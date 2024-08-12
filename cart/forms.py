from django import forms
from .models import  Order

class OrderCreationForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_option', 'delivery_address']