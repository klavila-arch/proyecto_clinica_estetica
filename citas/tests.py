from django.test import TestCase
from django.contrib.auth.models import User

from .models import Servicio


# ============================================
# PRUEBAS DE HUMO - SERVICIO / ORM
# ============================================

class ServicioORMTest(TestCase):

    def setUp(self):
        """Configuración de datos iniciales para las pruebas"""

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
    # PRUEBA 4 - DELETE
    # ========================================

    def test_eliminar_servicio(self):

        servicio_id = self.servicio.id

        self.servicio.delete()

        existe = Servicio.objects.filter(
            id=servicio_id
        ).exists()

        self.assertFalse(existe)


# ============================================
# PRUEBAS DE HUMO - ADMIN / CSV
# ============================================

class SmokeTests(TestCase):

    def setUp(self):
        """Configuración de datos iniciales para las pruebas"""

        self.servicio = Servicio.objects.create(
            nombre="Limpieza facial",
            descripcion="Servicio utilizado para pruebas del administrador.",
            precio=850.00,
            duracion=60,
            activo=True
        )

        self.user = User.objects.create_superuser(
            username="admin_test",
            email="admin@test.com",
            password="password123"
        )

    # ========================================
    # PRUEBA 5 - CREACIÓN DE SERVICIO
    # ========================================

    def test_creacion_servicio(self):
        """Verifica que el servicio se guarde correctamente"""

        self.assertEqual(
            Servicio.objects.count(),
            1
        )

        self.assertEqual(
            self.servicio.nombre,
            "Limpieza facial"
        )

    # ========================================
    # PRUEBA 6 - ACCESO AL IMPORTADOR CSV
    # ========================================

    def test_acceso_admin_importar_csv(self):
        """Verifica que la vista de importación CSV responda con HTTP 200"""

        self.client.login(
            username="admin_test",
            password="password123"
        )

        response = self.client.get(
            "/admin/citas/servicio/importar-csv/"
        )

        self.assertEqual(
            response.status_code,
            200
        )