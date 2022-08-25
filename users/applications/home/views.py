import datetime
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin # mixin to redirect user when it's not login
from django.views.generic import TemplateView
from django.urls import reverse_lazy

class FechaMixin(object):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fecha"] = datetime.datetime.now()
        return context
    

class HomePage(LoginRequiredMixin, TemplateView):
    template_name = 'home/index.html'
    login_url = reverse_lazy('users_app:user-login') # attr necessary to redirect


class TemplatePruebaMixin(FechaMixin, TemplateView):
    template_name = "home/mixin.html"
    