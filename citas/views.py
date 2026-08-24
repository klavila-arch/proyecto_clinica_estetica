from django.shortcuts import render


def inicio_view(request):
    return render(request, "citas/inicio.html")


def login_view(request):
    return render(request, "citas/login.html")