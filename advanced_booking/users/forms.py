import datetime

from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    birthday = forms.DateField(initial=datetime.date.today)
    accept_tos = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = [
            'email', 
            'username',
            'password1',
            'password2',
            'birthday',
            'accept_tos',
        ]