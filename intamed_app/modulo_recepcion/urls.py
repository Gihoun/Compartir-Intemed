from django.contrib import admin
from django.urls import path
from .views import inicio, ingresarPago, filtro_pacientes, editar_paciente, anularHora, genpdf_boleta, ingresarPac, tomar_hora, vista_boleta

app_name="modulo_recepcion"

urlpatterns = [   
    path('inicio/',inicio,name="inicio"),
    path('inicio/ingresarPac',ingresarPac, name="ingresarPac"),
    path('inicio/buscarPac',filtro_pacientes, name="buscarPac"),
    path('inicio/ingresarPago',ingresarPago, name="ingresarPag"),
    path('inicio/editarPac/<id>',editar_paciente, name="editarPac"),
    path('inicio/anularHora',anularHora, name="anularHor"),
    path('inicio/boleta',vista_boleta, name="boleta"),
    path('inicio/tomarHora/',tomar_hora, name="tomar_hr")
]