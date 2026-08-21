from django.contrib import admin
from .models import Servicio, Cliente, Empleado, Cita
from django import forms




admin.site.site_header = "Administración | Clínica Estética"
admin.site.site_title = "Clínica Estética"
admin.site.index_title = "Panel de administración"


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "precio",
        "duracion",
        "activo",
    )
    list_filter = ("activo",)
    search_fields = ("nombre",)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "apellido",
        "telefono",
        "correo",
    )
    search_fields = (
        "nombre",
        "apellido",
        "correo",
    )


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "apellido",
        "especialidad",
        "telefono",
        "activo",
    )
    list_filter = (
        "especialidad",
        "activo",
    )
    search_fields = (
        "nombre",
        "apellido",
        "especialidad",
    )


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    form = CitaAdminForm

    list_display = (
        "id",
        "cliente",
        "servicio",
        "empleado",
        "fecha",
        "hora",
        "estado",
    )

    list_filter = (
        "estado",
        "fecha",
        "servicio",
    )

    search_fields = (
        "cliente__nombre",
        "cliente__apellido",
        "servicio__nombre",
    )
    
class CitaAdminForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = "__all__"

        widgets = {
            "fecha": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
            "hora": forms.TimeInput(
                attrs={
                    "type": "time"
                }
            ),
        }    