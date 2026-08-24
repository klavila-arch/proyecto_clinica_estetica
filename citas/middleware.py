class AuditoriaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(
            f"[AUDITORÍA] Método: {request.method} | "
            f"Ruta: {request.path}"
        )

        response = self.get_response(request)

        print(
            f"[AUDITORÍA] Estado de respuesta: "
            f"{response.status_code}"
        )

        return response