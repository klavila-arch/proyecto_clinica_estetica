from django.test import TestCase

from .models import Servicio


# ============================================
# PRUEBAS DE HUMO - SERVICIO / ORM
# ============================================

class ServicioORMTest(TestCase):

    # ========================================
    # DATOS INICIALES PARA LAS PRUEBAS
    # ========================================

    def setUp(self):

        self.servicio = Servicio.objects.create(
            nombre="Limpieza facial de prueba",
            descripcion="Servicio utilizado para pruebas de humo.",
            precio=850.00,
            duracion=60,
            activo=True
        )


    # ========================================
    # PRUEBA 1 - CREATE
    # ========================================

    def test_crear_servicio(self):

        servicio = Servicio.objects.create(
            nombre="Masaje facial de prueba",
            descripcion="Prueba de creación mediante ORM.",
            precio=750.00,
            duracion=45,
            activo=True
        )

        self.assertIsNotNone(servicio.id)

        self.assertEqual(
            servicio.nombre,
            "Masaje facial de prueba"
        )


    # ========================================
    # PRUEBA 2 - READ
    # ========================================

    def test_consultar_servicio(self):

        servicio = Servicio.objects.get(
            id=self.servicio.id
        )

        self.assertEqual(
            servicio.nombre,
            "Limpieza facial de prueba"
        )

        self.assertEqual(
            float(servicio.precio),
            850.00
        )


    # ========================================
    # PRUEBA 3 - UPDATE
    # ========================================

    def test_actualizar_servicio(self):

        self.servicio.precio = 950.00
        self.servicio.duracion = 70

        self.servicio.save()

        servicio_actualizado = Servicio.objects.get(
            id=self.servicio.id
        )

        self.assertEqual(
            float(servicio_actualizado.precio),
            950.00
        )

        self.assertEqual(
            servicio_actualizado.duracion,
            70
        )


    # ========================================
        # ========================================
    # PRUEBA 4 - DELETE
    # ========================================

    def test_eliminar_servicio(self):

        servicio_id = self.servicio.id

        self.servicio.delete()

        existe = Servicio.objects.filter(
            id=servicio_id
        ).exists()

        self.assertFalse(existe)