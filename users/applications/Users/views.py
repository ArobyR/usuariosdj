from django.core.mail import send_mail
from django.views.generic import View, CreateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from django.views.generic.edit import (
    FormView
)
from .models import User
from .forms import (
    UserRegisterForm,
    LoginForm,
    UpdatePasswordForm,
    VerificationForm,
)
from .functions import code_generator


class UserRegisterView(FormView):
    template_name = 'users/register.html'

    form_class = UserRegisterForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):
        # generamos el codigo

        codigo = code_generator()

        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            # extra fields
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            coderegistro=codigo
        )

        # enviar el codigo al email del usuario
        subject = 'Confirmacion email'
        message = 'Codigo de verificacion: ' + codigo
        email_remitente = 'aroby.rosario@growit.com.do'

        send_mail(subject, message, email_remitente,
                  [form.cleaned_data['email'], ])

        # return super(UserRegisterView, self).form_valid(form)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification',
                kwargs={'pk': usuario.id}
            )  # facilita navegar entre las urls
        )


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


class CodeVerificationView(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:user-login')

    def get_form_kwargs(self):
        """ sobre escribe el metodo que recibe las kwargs en las vistas"""
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk']
        })
        return kwargs

    def form_valid(self, form):
        #
        # id_user = self.kwargs['pk']
        #
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )

        return super(CodeVerificationView, self).form_valid(form)
