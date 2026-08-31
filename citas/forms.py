from django import forms
from django.core.exceptions import ValidationError

from .models import Servicio


# ============================================
# FORMULARIO DE SERVICIOS
# ============================================

class ServicioForm(forms.ModelForm):

    class Meta:
        model = Servicio

        fields = [
            "nombre",
            "descripcion",
            "precio",
            "duracion",
            "activo",
        ]


    # ============================================
    # VALIDACIÓN INDIVIDUAL DEL NOMBRE
    # ============================================

    def clean_nombre(self):

        nombre = self.cleaned_data.get("nombre")

        if nombre:

            # Eliminar espacios al inicio y al final
            nombre = nombre.strip()

            # Validar longitud mínima
            if len(nombre) < 3:

                raise ValidationError(
                    "El nombre del servicio es demasiado corto "
                    "(mínimo 3 caracteres)."
                )

        # Normalizar el texto
        return nombre.title()


    # ============================================
    # VALIDACIÓN DEL PRECIO
    # ============================================

    def clean_precio(self):

        precio = self.cleaned_data.get("precio")

        if precio is not None and precio <= 0:

            raise ValidationError(
                "El precio debe ser mayor a cero."
            )

        return precio


    # ============================================
    # VALIDACIÓN DE DURACIÓN
    # ============================================

    def clean_duracion(self):

        duracion = self.cleaned_data.get("duracion")

        if duracion is not None and duracion <= 0:

            raise ValidationError(
                "La duración debe ser mayor a cero minutos."
            )

        return duracion


    # ============================================
    # VALIDACIÓN ENTRE NOMBRE Y PRECIO
    # ============================================

    def clean(self):

        cleaned_data = super().clean()

        nombre = cleaned_data.get("nombre")
        precio = cleaned_data.get("precio")

        # Regla de negocio:
        # La depilación láser no puede costar menos de $500 MXN.

        if (
            nombre
            and precio is not None
            and nombre.lower() == "depilación láser"
            and precio < 500
        ):

            raise ValidationError(
                "El servicio de Depilación láser no puede costar "
                "menos de $500 MXN."
            )

        return cleaned_data