from allauth.account.forms import SignupForm
from .models import User, OneTimeCode
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class NewUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class OneTimeCodeForm(forms.Form):
    username = forms.CharField(max_length=30)
    code = forms.CharField(max_length=30)