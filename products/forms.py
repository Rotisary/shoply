from .models import Review, Reply
from django import forms
from django.conf import settings


class ReviewForm(forms.ModelForm):
    body = forms.CharField(max_length=200)

    class Meta:
        model = Review
        fields = ['body']


class ReplyForm(forms.ModelForm):
    text = forms.CharField(max_length=200)

    class Meta:
        model = Reply
        fields = ['text']