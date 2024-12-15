from django import forms
from django.core.exceptions import ValidationError


class ContactForm(forms.Form):

    name = forms.CharField(max_length=100, label="Ваше имя")

    email = forms.EmailField(label="Ваш Email")

    message = forms.CharField(widget=forms.Textarea, label="Сообщение")


class CustomContactForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)
    email = forms.EmailField(label='Ваш email')
    message = forms.CharField(label='Сообщение', widget=forms.Textarea)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@example.com'):
            raise ValidationError('Email должен заканчиваться на @example.com')
        return email
