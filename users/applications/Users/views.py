from cmath import log
from django.shortcuts import render
from django.views.generic import View, CreateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from django.views.generic.edit import (
    FormView
)
from .models import User
from .forms import  (
    UserRegisterForm, 
    LoginForm,
   UpdatePasswordForm
) 


class UserRegisterView(FormView):
    template_name = 'users/register.html'

    form_class = UserRegisterForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):
        #
        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            # extra fields
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
        )

        return super(UserRegisterView, self).form_valid(form)


class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        login(self.request, user)

        return super(LoginUser, self).form_valid(form)


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)

        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )  # facilita navegar entre las urls
        )


class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')
    
    def form_valid(self, form):
        user = self.request.user
        user_auth = authenticate(
            username=user.username,
            password=form.cleaned_data['password'],
        )

        if user_auth:
            new_password = form.cleaned_data['password2']
            user.set_password(new_password)
            user.save()
             
        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)