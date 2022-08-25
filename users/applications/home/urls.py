from . import views
from django.urls import path

app_name = "home_app"

urlpatterns = [
    path(
        'panel/',
        views.HomePage.as_view(),
        name="panel"
    ),
    path(
        'mixin/',
        views.TemplatePruebaMixin.as_view(),
        name="mixin"
    ),
]
