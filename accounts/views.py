from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm
