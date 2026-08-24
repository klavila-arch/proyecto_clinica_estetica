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

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del servicio",
                }
            ),

            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Descripción del servicio",
                }
            ),

            "precio": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "duracion": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "activo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]

        nombre = nombre.strip().title()

        return nombre

    def clean_precio(self):
        precio = self.cleaned_data["precio"]

        if precio <= 0:
            raise ValidationError(
                "El precio debe ser mayor a cero."
            )

        return precio

    def clean_duracion(self):
        duracion = self.cleaned_data["duracion"]

        if duracion <= 0:
            raise ValidationError(
                "La duración debe ser mayor a cero."
            )

        return duracion