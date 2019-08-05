from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from accounts.forms import RegisterForm

class LoginView(LoginView):
    
    template_name = 'accounts/user/user_login.html'

class LogoutView(LogoutView):
    
    template_name = 'accounts/user/user_logout.html'
    
class RegisterUserView(CreateView):
    
    model = User
    template_name = "accounts/user/user_register.html"
    success_url = '/accounts/login/'
    form_class = RegisterForm
    context_object_name = 'user'

    def get_success_url(self):
        if self.success_url:
            url = self.success_url
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url
