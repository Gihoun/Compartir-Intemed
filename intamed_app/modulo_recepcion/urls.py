from django.contrib import admin
from django.urls import path
from .views import inicio, ingresarPago, filtro_pacientes, editar_paciente, anularHora, genpdf_boleta, tomar_hora

app_name="modulo_recepcion"

urlpatterns = [   
    path('inicio/ingresarPac',inicio, name="ingresarPac"),
    path('inicio/buscarPac',filtro_pacientes, name="buscarPac"),
    path('inicio/ingresarPago',ingresarPago, name="ingresarPag"),
    path('inicio/editarPac/<id>',editar_paciente, name="editarPac"),
    path('inicio/anularHora',anularHora, name="anularHor"),
    path('inicio/genboleta/<id>',genpdf_boleta, name="genpdf"),
    path('inicio/tomarHora/',tomar_hora, name="tomar_hr")
]