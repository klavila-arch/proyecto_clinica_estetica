import csv
import io

from decimal import Decimal, InvalidOperation

from django import forms
from django.contrib import admin, messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import path

from .models import Servicio, Cliente, Empleado, Cita


# ============================================
# PERSONALIZACIÓN DEL PANEL ADMINISTRATIVO
# ============================================

admin.site.site_header = "Administración | Clínica Estética"
admin.site.site_title = "Panel Clínica Estética"
admin.site.index_title = "Control de Operaciones"


# ============================================
# FORMULARIO PARA IMPORTAR CSV
# ============================================

class CsvImportForm(forms.Form):
    csv_file = forms.FileField(
        label="Selecciona un archivo CSV"
    )


# ============================================
# SERVICIOS
# ============================================

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nombre",
        "precio",
        "duracion",
        "activo",
    )

    list_filter = (
        "activo",
    )

    search_fields = (
        "nombre",
    )

    actions = [
        "cargar_csv_action",
    ]

    # ========================================
    # URL PERSONALIZADA PARA IMPORTAR CSV
    # ========================================

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "importar-csv/",
                self.admin_site.admin_view(self.importar_csv),
                name="importar_csv_servicios",
            ),
        ]

        return custom_urls + urls

    # ========================================
    # IMPORTAR SERVICIOS DESDE CSV
    # ========================================

    def importar_csv(self, request):

        if request.method == "POST":

            form = CsvImportForm(
                request.POST,
                request.FILES
            )

            if form.is_valid():

                csv_file = request.FILES["csv_file"]

                # ----------------------------------------
                # VALIDAR EXTENSIÓN
                # ----------------------------------------

                if not csv_file.name.lower().endswith(".csv"):

                    messages.error(
                        request,
                        "El archivo debe tener extensión .csv"
                    )

                    return redirect(".")

                try:

                    # ----------------------------------------
                    # LEER ARCHIVO
                    # utf-8-sig elimina BOM de Excel
                    # ----------------------------------------

                    contenido = csv_file.read().decode(
                        "utf-8-sig"
                    )

                    # ----------------------------------------
                    # DETECTAR SEPARADOR
                    # ----------------------------------------

                    try:

                        dialect = csv.Sniffer().sniff(
                            contenido[:2048],
                            delimiters=";,"
                        )

                        separador = dialect.delimiter

                    except csv.Error:

                        separador = ","

                    archivo = io.StringIO(contenido)

                    lector = csv.reader(
                        archivo,
                        delimiter=separador
                    )

                    # ----------------------------------------
                    # OMITIR ENCABEZADOS
                    # ----------------------------------------

                    next(lector, None)

                    contador_creados = 0
                    contador_actualizados = 0

                    # ----------------------------------------
                    # TRANSACCIÓN
                    # ----------------------------------------

                    with transaction.atomic():

                        for numero_fila, row in enumerate(
                            lector,
                            start=2
                        ):

                            # --------------------------------
                            # IGNORAR FILAS VACÍAS
                            # --------------------------------

                            if not row:
                                continue

                            if all(
                                not str(campo).strip()
                                for campo in row
                            ):
                                continue

                            # --------------------------------
                            # VALIDAR COLUMNAS
                            # --------------------------------

                            if len(row) < 5:

                                raise ValueError(
                                    f"La fila {numero_fila} "
                                    f"no contiene las 5 columnas "
                                    f"requeridas."
                                )

                            # --------------------------------
                            # OBTENER DATOS
                            # --------------------------------

                            nombre = row[0].strip()

                            descripcion = row[1].strip()

                            precio_texto = (
                                row[2]
                                .strip()
                                .replace("$", "")
                                .replace(" ", "")
                            )

                            duracion_texto = (
                                row[3]
                                .strip()
                            )

                            activo_texto = (
                                row[4]
                                .strip()
                                .lower()
                            )

                            # --------------------------------
                            # VALIDAR NOMBRE
                            # --------------------------------

                            if not nombre:

                                raise ValueError(
                                    f"La fila {numero_fila} "
                                    f"no tiene nombre."
                                )

                            # --------------------------------
                            # VALIDAR PRECIO
                            # --------------------------------

                            if not precio_texto:

                                raise ValueError(
                                    f"La fila {numero_fila} "
                                    f"no tiene precio."
                                )

                            # Si Excel usa coma decimal
                            if (
                                separador == ";"
                                and "," in precio_texto
                                and "." not in precio_texto
                            ):
                                precio_texto = (
                                    precio_texto.replace(",", ".")
                                )

                            try:

                                precio = Decimal(
                                    precio_texto
                                )

                            except InvalidOperation:

                                raise ValueError(
                                    f"El precio de la fila "
                                    f"{numero_fila} no es válido: "
                                    f"{row[2]}"
                                )

                            # --------------------------------
                            # VALIDAR DURACIÓN
                            # --------------------------------

                            if not duracion_texto:

                                raise ValueError(
                                    f"La fila {numero_fila} "
                                    f"no tiene duración."
                                )

                            try:

                                duracion = int(
                                    float(
                                        duracion_texto.replace(
                                            ",",
                                            "."
                                        )
                                    )
                                )

                            except ValueError:

                                raise ValueError(
                                    f"La duración de la fila "
                                    f"{numero_fila} no es válida: "
                                    f"{row[3]}"
                                )

                            # --------------------------------
                            # CONVERTIR ACTIVO
                            # --------------------------------

                            activo = activo_texto in [
                                "true",
                                "1",
                                "si",
                                "sí",
                                "activo",
                                "yes",
                            ]

                            # --------------------------------
                            # BUSCAR SERVICIO EXISTENTE
                            # --------------------------------

                            servicios_existentes = (
                                Servicio.objects.filter(
                                    nombre__iexact=nombre
                                )
                            )

                            servicio_existente = (
                                servicios_existentes.first()
                            )

                            # --------------------------------
                            # SI YA EXISTE, ACTUALIZAR
                            # --------------------------------

                            if servicio_existente:

                                servicio_existente.descripcion = (
                                    descripcion
                                )

                                servicio_existente.precio = (
                                    precio
                                )

                                servicio_existente.duracion = (
                                    duracion
                                )

                                servicio_existente.activo = (
                                    activo
                                )

                                servicio_existente.save()

                                contador_actualizados += 1

                            # --------------------------------
                            # SI NO EXISTE, CREAR
                            # --------------------------------

                            else:

                                Servicio.objects.create(
                                    nombre=nombre,
                                    descripcion=descripcion,
                                    precio=precio,
                                    duracion=duracion,
                                    activo=activo,
                                )

                                contador_creados += 1

                    # ----------------------------------------
                    # MENSAJE DE ÉXITO
                    # ----------------------------------------

                    messages.success(
                        request,
                        (
                            f"Importación completada. "
                            f"Servicios creados: "
                            f"{contador_creados}. "
                            f"Servicios actualizados: "
                            f"{contador_actualizados}."
                        )
                    )

                    return redirect(
                        "admin:citas_servicio_changelist"
                    )

                except Exception as error:

                    messages.error(
                        request,
                        f"Error al importar el archivo: {error}"
                    )

        else:

            form = CsvImportForm()

        # ========================================
        # CONTEXTO
        # ========================================

        context = {
            **self.admin_site.each_context(request),
            "form": form,
            "title": "Importar servicios desde CSV",
        }

        return render(
            request,
            "admin/citas/servicio/importar_csv.html",
            context
        )

    # ========================================
    # ACCIÓN DEL ADMIN
    # ========================================

    @admin.action(
        description="Cargar servicios desde archivo CSV"
    )
    def cargar_csv_action(
        self,
        request,
        queryset
    ):

        return redirect(
            "admin:importar_csv_servicios"
        )


# ============================================
# CLIENTES
# ============================================

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
        "telefono",
    )


# ============================================
# EMPLEADOS
# ============================================

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


# ============================================
# CITAS
# ============================================

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):

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
    )

    search_fields = (
        "cliente__nombre",
        "cliente__apellido",
        "servicio__nombre",
        "empleado__nombre",
        "empleado__apellido",
    )