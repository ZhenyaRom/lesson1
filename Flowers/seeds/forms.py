from django import forms


# Класс для отправки сообщений
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Ваше имя")
    email = forms.EmailField(label="Ваш Email")
    message = forms.CharField(widget=forms.Textarea, label="Сообщение")
