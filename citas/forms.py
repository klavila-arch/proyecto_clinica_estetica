from django import forms
from django.core.exceptions import ValidationError
from .models import Servicio


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
            nombre = nombre.strip()

            if len(nombre) < 3:
                raise ValidationError(
                    "El nombre del servicio es demasiado corto "
                    "(mínimo 3 caracteres)."
                )

        # Elimina espacios sobrantes y aplica formato título
        return nombre.title()


    # ============================================
    # VALIDACIÓN ENTRE NOMBRE Y PRECIO
    # ============================================

    def clean(self):
        cleaned_data = super().clean()

        nombre = cleaned_data.get("nombre")
        precio = cleaned_data.get("precio")

        # Regla de negocio entre dos campos
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