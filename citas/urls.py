from django.urls import path
from . import views


urlpatterns = [
    path("", views.inicio_view, name="inicio"),
    path("login/", views.login_view, name="login"),
]