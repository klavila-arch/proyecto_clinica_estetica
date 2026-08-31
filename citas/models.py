from django.db import models
from django.core.exceptions import ValidationError


# ============================================
# VALIDACIONES
# ============================================

def validar_precio_positivo(valor):
    if valor <= 0:
        raise ValidationError(
            "El precio debe ser mayor a cero."
        )


# ============================================
# SERVICIO
# ============================================

class Servicio(models.Model):

    nombre = models.CharField(
        max_length=100
    )

    descripcion = models.TextField(
        blank=True
    )

    precio = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[validar_precio_positivo]
    )

    duracion = models.PositiveIntegerField(
        help_text="Duración del servicio en minutos"
    )

    activo = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


# ============================================
# CLIENTE
# ============================================

class Cliente(models.Model):

    nombre = models.CharField(
        max_length=100
    )

    apellido = models.CharField(
        max_length=100
    )

    telefono = models.CharField(
        max_length=20
    )

    correo = models.EmailField(
        unique=True
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# ============================================
# EMPLEADO
# ============================================

class Empleado(models.Model):

    nombre = models.CharField(
        max_length=100
    )

    apellido = models.CharField(
        max_length=100
    )

    especialidad = models.CharField(
        max_length=100
    )

    telefono = models.CharField(
        max_length=20,
        blank=True
    )

    activo = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# ============================================
# CITA
# ============================================

class Cita(models.Model):

    ESTADOS = [
        ("PENDIENTE", "Pendiente"),
        ("CONFIRMADA", "Confirmada"),
        ("COMPLETADA", "Completada"),
        ("CANCELADA", "Cancelada"),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="citas"
    )

    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        related_name="citas",
        null=True,
        blank=True
    )

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.SET_NULL,
        related_name="citas",
        null=True,
        blank=True
    )

    fecha = models.DateField()

    hora = models.TimeField()

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="PENDIENTE"
    )

    notas = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"Orden #{self.id} - {self.cliente} ({self.estado})"