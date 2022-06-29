from django.contrib import admin
from django.urls import path
from .views import inicio, mi_cuenta, anular_hr

app_name="modulo_paciente"

urlpatterns = [   
    path('inicio/<id>',inicio,name="indexPaciente"),
    path('cuenta/<id>',mi_cuenta,name="micuenta"),
    path('anular/<id>',anular_hr,name="anular")
]