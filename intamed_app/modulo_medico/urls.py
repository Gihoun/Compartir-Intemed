from unicodedata import name
from django.contrib import admin
from django.urls import path
from .views import inicio,atePaciente,agenda,consultaV,consultaP,examenesP,receta_test,receta_med
app_name="modulo_medico"

urlpatterns = [   
    path('inicio/',inicio,name="index"),
    path('AtencionPaciente/<id>',atePaciente,name="atePaciente"),
    path('agenda_paciente/',agenda,name="agenda_pa"),
    path('consulta_paciente/',consultaV,name="consulta"),
    path('consulta_paciente/<id>',consultaP,name="consultaP"),
    path('examenes_paciente',examenesP,name="examenesP"),
    path('receta_paciente/<id>',receta_med,name="recetaP"),
    path('receta/',receta_test,name="recetaL"),
   
]