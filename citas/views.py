from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Servicio, Cita
from .forms import ServicioForm, NuevaCitaForm
from .citadao import CitaDAO


def es_administrador(user):
    return (
        user.is_authenticated
        and (
            user.groups.filter(name="Administrador").exists()
            or user.is_superuser
        )
    )


def es_empleado(user):
    return (
        user.is_authenticated
        and (
            user.groups.filter(name="Empleado").exists()
            or user.groups.filter(name="Administrador").exists()
            or user.is_superuser
        )
    )


def es_cliente(user):
    return (
        user.is_authenticated
        and (
            user.groups.filter(name="Cliente").exists()
            or user.is_superuser
        )
    )


def inicio_view(request):
    return render(
        request,
        "citas/inicio.html"
    )


def login_view(request):
    return render(
        request,
        "citas/login.html"
    )


def servicios_view(request):
    servicios = Servicio.objects.all()

    return render(
        request,
        "citas/servicios.html",
        {
            "servicios": servicios
        }
    )


@login_required(login_url="/admin/login/")
@user_passes_test(
    es_administrador,
    login_url="/admin/login/"
)
def crear_servicio(request):

    if request.method == "POST":

        form = ServicioForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "El servicio fue creado correctamente."
            )

            return redirect("servicios")

    else:
        form = ServicioForm()

    return render(
        request,
        "citas/servicio_form.html",
        {
            "form": form,
            "titulo": "Agregar servicio"
        }
    )


@login_required(login_url="/admin/login/")
@user_passes_test(
    es_administrador,
    login_url="/admin/login/"
)
def editar_servicio(
    request,
    servicio_id
):

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

            messages.success(
                request,
                "El servicio fue actualizado correctamente."
            )

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
            "titulo": "Editar servicio"
        }
    )


@login_required(login_url="/admin/login/")
@user_passes_test(
    es_administrador,
    login_url="/admin/login/"
)
def eliminar_servicio(
    request,
    servicio_id
):

    servicio = get_object_or_404(
        Servicio,
        id=servicio_id
    )

    if request.method == "POST":

        servicio.delete()

        messages.success(
            request,
            "El servicio fue eliminado correctamente."
        )

        return redirect("servicios")

    return render(
        request,
        "citas/servicio_confirmar_eliminar.html",
        {
            "servicio": servicio
        }
    )


@login_required(login_url="/admin/login/")
@user_passes_test(
    es_empleado,
    login_url="/admin/login/"
)
def gestion_citas(request):
    """
    Muestra únicamente las citas activas
    utilizando la capa DAO.
    """

    citas_activas = CitaDAO.obtener_activas()

    return render(
        request,
        "citas/gestion_citas.html",
        {
            "citas": citas_activas,
            "estados": Cita.ESTADOS
        }
    )


@login_required(login_url="/admin/login/")
@user_passes_test(
    es_empleado,
    login_url="/admin/login/"
)
def nueva_cita(request):
    """
    Permite registrar una nueva cita
    desde el frontend utilizando el DAO.
    """

    if request.method == "POST":

        form = NuevaCitaForm(request.POST)

        if form.is_valid():

            cita = CitaDAO.crear_cita(
                cliente_id=form.cleaned_data["cliente"].id,
                servicio_id=form.cleaned_data["servicio"].id,
                empleado_id=form.cleaned_data["empleado"].id,
                fecha=form.cleaned_data["fecha"],
                hora=form.cleaned_data["hora"],
                notas=form.cleaned_data["notas"]
            )

            if cita:

                messages.success(
                    request,
                    f"¡Cita registrada correctamente "
                    f"para {cita.cliente}!"
                )

                return redirect(
                    "gestion_citas"
                )

            else:

                messages.error(
                    request,
                    "Ocurrió un problema al registrar la cita."
                )

    else:

        form = NuevaCitaForm()

    return render(
        request,
        "citas/nueva_cita.html",
        {
            "form": form
        }
    )


@login_required(login_url="/admin/login/")
@user_passes_test(
    es_empleado,
    login_url="/admin/login/"
)
def actualizar_estado_cita(
    request,
    cita_id
):
    """
    Actualiza el estado de una cita
    desde la vista web utilizando el DAO.
    """

    if request.method == "POST":

        nuevo_estado = request.POST.get(
            "estado"
        )

        estados_validos = [
            estado[0]
            for estado in Cita.ESTADOS
        ]

        if nuevo_estado in estados_validos:

            cita = CitaDAO.cambiar_estado(
                cita_id,
                nuevo_estado
            )

            if cita:

                messages.success(
                    request,
                    f"La cita #{cita.id} fue actualizada a "
                    f"{cita.get_estado_display()}."
                )

            else:

                messages.error(
                    request,
                    "No se encontró la cita."
                )

        else:

            messages.error(
                request,
                "El estado seleccionado no es válido."
            )

    return redirect(
        "gestion_citas"
    )