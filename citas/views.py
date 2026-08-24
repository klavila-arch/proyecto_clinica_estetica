from django.shortcuts import render, redirect, get_object_or_404

from .models import Servicio
from .forms import ServicioForm


def inicio_view(request):
    return render(request, "citas/inicio.html")


def login_view(request):
    return render(request, "citas/login.html")


def servicios_view(request):
    servicios = Servicio.objects.all()

    return render(
        request,
        "citas/servicios.html",
        {
            "servicios": servicios
        }
    )


def crear_servicio_view(request):

    if request.method == "POST":
        form = ServicioForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("servicios")

    else:
        form = ServicioForm()

    return render(
        request,
        "citas/servicio_form.html",
        {
            "form": form,
            "titulo": "Agregar servicio",
        }
    )


def editar_servicio_view(request, servicio_id):

    servicio = get_object_or_404(
        Servicio,
        id=servicio_id
    )

    if request.method == "POST":

        form = ServicioForm(
            request.POST,
            instance=servicio
        )

        if form.is_valid():
            form.save()

            return redirect("servicios")

    else:
        form = ServicioForm(
            instance=servicio
        )

    return render(
        request,
        "citas/servicio_form.html",
        {
            "form": form,
            "titulo": "Editar servicio",
        }
    )


def eliminar_servicio_view(request, servicio_id):

    servicio = get_object_or_404(
        Servicio,
        id=servicio_id
    )

    if request.method == "POST":
        servicio.delete()

        return redirect("servicios")

    return render(
        request,
        "citas/servicio_confirmar_eliminar.html",
        {
            "servicio": servicio
        }
    )