from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.inicio_view,
        name="inicio"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "servicios/",
        views.servicios_view,
        name="servicios"
    ),

    path(
        "servicios/nuevo/",
        views.crear_servicio,
        name="crear_servicio"
    ),

    path(
        "servicios/<int:servicio_id>/editar/",
        views.editar_servicio,
        name="editar_servicio"
    ),

    path(
        "servicios/<int:servicio_id>/eliminar/",
        views.eliminar_servicio,
        name="eliminar_servicio"
    ),

    path(
        "gestion-citas/",
        views.gestion_citas,
        name="gestion_citas"
    ),

    path(
        "gestion-citas/nueva/",
        views.nueva_cita,
        name="nueva_cita"
    ),

    path(
        "gestion-citas/<int:cita_id>/estado/",
        views.actualizar_estado_cita,
        name="actualizar_estado_cita"
    ),
]