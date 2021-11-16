from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from account.forms import UserUpdateForm, ProfileUpdateForm
from account.models import User
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

from django.contrib import messages



class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'registration/signup.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('')
    success_message = 'User registered successfully!'

class SignInView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user)
    return render(request,'profile.html', { 'u_form':u_form, 'p_form':p_form })

