from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Servicio, Cita
from .forms import ServicioForm


# ============================================
# ROLES Y PERMISOS
# ============================================

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


# ============================================
# PÁGINA DE INICIO
# ============================================

def inicio_view(request):
    return render(request, "citas/inicio.html")


# ============================================
# LOGIN
# ============================================

def login_view(request):
    return render(request, "citas/login.html")


# ============================================
# CONSULTA DE SERVICIOS
# READ
# ============================================

def servicios_view(request):
    servicios = Servicio.objects.all()

    return render(
        request,
        "citas/servicios.html",
        {
            "servicios": servicios
        }
    )


# ============================================
# CREAR SERVICIO
# CREATE
# Solo Administrador
# ============================================

@login_required
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


# ============================================
# EDITAR SERVICIO
# UPDATE
# Solo Administrador
# ============================================

@login_required
@user_passes_test(
    es_administrador,
    login_url="/admin/login/"
)
def editar_servicio(request, servicio_id):

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


# ============================================
# ELIMINAR SERVICIO
# DELETE
# Solo Administrador
# ============================================

@login_required
@user_passes_test(
    es_administrador,
    login_url="/admin/login/"
)
def eliminar_servicio(request, servicio_id):

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


# ============================================
# GESTIÓN DE CITAS
# READ
# Administrador y Empleado
# ============================================

@login_required
@user_passes_test(
    es_empleado,
    login_url="/admin/login/"
)
def gestion_citas(request):

    citas = Cita.objects.select_related(
        "cliente",
        "servicio",
        "empleado"
    ).order_by(
        "fecha",
        "hora"
    )

    return render(
        request,
        "citas/gestion_citas.html",
        {
            "citas": citas,
            "estados": Cita.ESTADOS
        }
    )


# ============================================
# ACTUALIZAR ESTADO DE CITA
# UPDATE
# Administrador y Empleado
# ============================================

@login_required
@user_passes_test(
    es_empleado,
    login_url="/admin/login/"
)
def actualizar_estado_cita(request, cita_id):

    cita = get_object_or_404(
        Cita,
        id=cita_id
    )

    if request.method == "POST":

        nuevo_estado = request.POST.get(
            "estado"
        )

        estados_validos = [
            estado[0]
            for estado in Cita.ESTADOS
        ]

        if nuevo_estado in estados_validos:

            cita.estado = nuevo_estado

            cita.save()

            messages.success(
                request,
                f"La cita #{cita.id} fue actualizada a "
                f"{cita.get_estado_display()}."
            )

        else:

            messages.error(
                request,
                "El estado seleccionado no es válido."
            )

    return redirect(
        "gestion_citas"
    )