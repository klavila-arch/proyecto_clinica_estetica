from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio_view, name="inicio"),
    path("login/", views.login_view, name="login"),
    path("servicios/", views.servicios_view, name="servicios"),
    path("servicios/nuevo/", views.crear_servicio_view, name="crear_servicio"),
    path(
        "servicios/<int:servicio_id>/editar/",
        views.editar_servicio_view,
        name="editar_servicio"
    ),
    path(
        "servicios/<int:servicio_id>/eliminar/",
        views.eliminar_servicio_view,
        name="eliminar_servicio"
    ),
]