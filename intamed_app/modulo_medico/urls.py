from django.contrib import admin
from django.urls import path
from .views import inicio,atePaciente,agenda

urlpatterns = [   
    path('inicio/',inicio,name="index"),
    path('AtencionPaciente/<id>',atePaciente,name="atePaciente"),
    path('agenda_paciente/',agenda,name="agenda_pa")
]