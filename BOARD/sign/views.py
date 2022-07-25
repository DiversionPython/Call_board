from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
import random
from .models import OneTimeCode
from .forms import RegisterUserForm, LoginUserForm, OneTimeCodeForm


class BaseRegisterView(CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'sign/signup.html'
    success_url = reverse_lazy('ad')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        passw = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')
        user = authenticate(username=username, password=passw)
        OneTimeCode.objects.filter(user=user).delete()
        OneTimeCode.objects.create(code=random.choice('abcds'), user=user)
        code = OneTimeCode.objects.get(user=user)
        print(user.email)
        send_mail("Сообщение",
                  "Имя пользователя:{}, пароль:{}".format(user.username, code.code),
                  from_email='teststudymail@yandex.ru',
                  recipient_list=[email],
                  fail_silently=False)
        return redirect('login_next')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'sign/login.html'


def view_code(request):
    form = OneTimeCodeForm()
    return render(request, 'sign/login_next.html', {'form': form, 'title': 'Код проверки', })


def login_with_code_view(request):
    username = request.POST['username']
    code = request.POST['code']
    user = User.objects.get(username=username)
    if OneTimeCode.objects.filter(code=code, user=user).exists():
        user.save()
        login(request, user)
        OneTimeCode.objects.filter(user=user).delete()
    else:
        return render(request, 'sign/login_next.html', {'error': 'ошибка ввода имени или пароля', })
    return redirect('ad')

