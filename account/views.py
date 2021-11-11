from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from account.models import User
from .forms import RegistrationForm

class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'account/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')
    success_message = 'User registered successfully!'

class SignInView(LoginView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('home')

def profile(request):
    return render(request, 'account/profile.html')



