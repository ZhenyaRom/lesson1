from django import forms
from django.core.exceptions import ValidationError


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Ваше имя")
    email = forms.EmailField(label="Ваш Email")
    message = forms.CharField(widget=forms.Textarea, label="Сообщение")


class BuyerForm(forms.Form):
    login = forms.CharField(max_length=100, label="login")
    password = forms.CharField(min_length=8, max_length=30, label="Пароль")
    password_again = forms.CharField(min_length=8, max_length=30, label="Пароль")
    email = forms.EmailField(label="Ваш Email")



