from django import forms
from django.contrib.auth.forms import  AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import *

class LoginForm(AuthenticationForm):
    """Аутентификация пользователя"""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Пароль'}))

class RegistrationForm(UserCreationForm):
    """Регистрация пользователя"""
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Подтвердите Пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
                  'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Почта'})}


class ReviewForm(forms.ModelForm):
    """Форма для отзывов"""

    class Meta:
        model = Review
        fields = ('text', )
        widget = {'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ваш отзыв'})}


class CustomerForm(forms.ModelForm):
    """Контактная информация"""

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'phone')
        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ivan@ivanov.ru'}),
                   'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+375291234567'})
                   }



class ShippingForm(forms.ModelForm):
    """Адрес доставки"""

    class Meta:
        model = ShippingAddress

        fields = ('country', 'city', 'state', 'street')
        widgets = {'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Беларусь'}),
                   'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Минск'}),
                   'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Минская'}),
                   'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Дом/Улица/Фонарь/Аптека'})
                   }



