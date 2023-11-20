from django import forms
from .models import CartItems, Order

class OrderCreationForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_option', 'delivery_address']