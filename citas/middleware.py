# ============================================
# MIDDLEWARE DE AUDITORÍA
# ============================================

class AuditoriaMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Registrar información de la solicitud
        print(
            f"[AUDITORÍA] Método: {request.method} | "
            f"Ruta: {request.path}"
        )

        # Procesar la solicitud
        response = self.get_response(request)

        # Registrar el código de respuesta
        print(
            f"[AUDITORÍA] Estado de respuesta: "
            f"{response.status_code}"
        )

        return response