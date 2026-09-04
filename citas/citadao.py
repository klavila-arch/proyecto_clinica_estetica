from typing import Optional

from .models import Cita, Cliente, Servicio, Empleado


class CitaDAO:
    """Capa DAO para operaciones relacionadas con las citas."""

    @staticmethod
    def obtener_todas():
        """
        Obtiene todas las citas registradas.
        """
        return Cita.objects.select_related(
            "cliente",
            "servicio",
            "empleado"
        ).order_by("fecha", "hora")

    @staticmethod
    def obtener_activas():
        """
        Obtiene únicamente las citas activas:
        PENDIENTE y CONFIRMADA.
        """
        return Cita.objects.select_related(
            "cliente",
            "servicio",
            "empleado"
        ).filter(
            estado__in=[
                "PENDIENTE",
                "CONFIRMADA"
            ]
        ).order_by("fecha", "hora")

    @staticmethod
    def cambiar_estado(
        cita_id: int,
        nuevo_estado: str
    ) -> Optional[Cita]:
        """
        Cambia el estado de una cita.
        """
        try:
            cita = Cita.objects.get(id=cita_id)

            cita.estado = nuevo_estado
            cita.save()

            return cita

        except Cita.DoesNotExist:
            return None

    @staticmethod
    def crear_cita(
        cliente_id: int,
        servicio_id: int,
        empleado_id: int,
        fecha,
        hora,
        notas: str = ""
    ) -> Optional[Cita]:
        """
        Crea una nueva cita relacionada con
        cliente, servicio y empleado.
        """
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            servicio = Servicio.objects.get(id=servicio_id)
            empleado = Empleado.objects.get(id=empleado_id)

            cita = Cita.objects.create(
                cliente=cliente,
                servicio=servicio,
                empleado=empleado,
                fecha=fecha,
                hora=hora,
                estado="PENDIENTE",
                notas=notas
            )

            return cita

        except (
            Cliente.DoesNotExist,
            Servicio.DoesNotExist,
            Empleado.DoesNotExist
        ):
            return None