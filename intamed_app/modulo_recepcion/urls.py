from django.contrib import admin
from django.urls import path
from .views import inicio, buscarPaciente, ingresarPago

urlpatterns = [   
    path('inicio/ingresarPac',inicio, name="ingresarPac"),
    path('inicio/buscarPac',buscarPaciente, name="buscarPac"),
    path('inicio/ingresarPago',ingresarPago, name="ingresarPag")
]