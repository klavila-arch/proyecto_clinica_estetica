from django import forms

from .models import Servicio, Cliente, Empleado


class ServicioForm(forms.ModelForm):

    class Meta:
        model = Servicio
        fields = [
            "nombre",
            "descripcion",
            "precio",
            "duracion",
            "activo"
        ]

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre", "").strip()

        if len(nombre) < 3:
            raise forms.ValidationError(
                "El nombre debe tener al menos 3 caracteres."
            )

        return nombre.title()

    def clean_precio(self):
        precio = self.cleaned_data.get("precio")

        if precio is not None and precio <= 0:
            raise forms.ValidationError(
                "El precio debe ser mayor a cero."
            )

        return precio

    def clean_duracion(self):
        duracion = self.cleaned_data.get("duracion")

        if duracion is not None and duracion <= 0:
            raise forms.ValidationError(
                "La duración debe ser mayor a cero."
            )

        return duracion

    def clean(self):
        cleaned_data = super().clean()

        nombre = cleaned_data.get("nombre")
        precio = cleaned_data.get("precio")

        if (
            nombre
            and precio
            and nombre.lower() == "depilación láser"
            and precio < 500
        ):
            self.add_error(
                "precio",
                "El servicio de Depilación láser "
                "no puede costar menos de $500 MXN."
            )

        return cleaned_data


class NuevaCitaForm(forms.Form):

    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        label="Cliente"
    )

    servicio = forms.ModelChoiceField(
        queryset=Servicio.objects.filter(activo=True),
        label="Servicio"
    )

    empleado = forms.ModelChoiceField(
        queryset=Empleado.objects.filter(activo=True),
        label="Empleado"
    )

    fecha = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(
            attrs={
                "type": "date"
            }
        )
    )

    hora = forms.TimeField(
        label="Hora",
        widget=forms.TimeInput(
            attrs={
                "type": "time"
            }
        )
    )

    notas = forms.CharField(
        label="Notas",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3
            }
        )
    )