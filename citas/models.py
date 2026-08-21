from django.db import models


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    duracion = models.PositiveIntegerField(
        help_text="Duración del servicio en minutos"
    )
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Cita(models.Model):
    ESTADOS = [
        ("PENDIENTE", "Pendiente"),
        ("CONFIRMADA", "Confirmada"),
        ("COMPLETADA", "Completada"),
        ("CANCELADA", "Cancelada"),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )

    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE
    )

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.SET_NULL,
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

    notas = models.TextField(blank=True)

    def __str__(self):
        return f"{self.cliente} - {self.servicio} - {self.fecha}"

# Create your models here.
