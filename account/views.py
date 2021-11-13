from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from account.models import User
from .forms import RegistrationForm

class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'registration/signup.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('')
    success_message = 'User registered successfully!'

class SignInView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('')

def profile(request):
    return render(request, 'profile/myprofile.html')



