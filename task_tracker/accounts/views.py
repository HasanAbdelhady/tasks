from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, TemplateView, RedirectView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView


class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('admin_dashboard')
        return reverse_lazy('assignee_view')

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form, error='Invalid credentials')
        )


class LoginOrSignupView(TemplateView):
    template_name = 'login_or_signup.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('admin_dashboard')
            return redirect('assignee_view')
        return super().get(request, *args, **kwargs)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login_or_signup')
