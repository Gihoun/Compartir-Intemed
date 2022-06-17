from django.contrib import admin
from django.urls import path
from .views import inicio, ingresarPago, filtro_pacientes, editar_paciente

urlpatterns = [   
    path('inicio/ingresarPac',inicio, name="ingresarPac"),
    path('inicio/buscarPac',filtro_pacientes, name="buscarPac"),
    path('inicio/ingresarPago',ingresarPago, name="ingresarPag"),
    path('inicio/editararPac/<id>',editar_paciente, name="editarPac"),
]