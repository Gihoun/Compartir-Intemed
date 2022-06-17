from django.contrib import admin
from django.urls import path
from .views import inicio, mi_cuenta

urlpatterns = [   
    path('inicio/<id>',inicio,name="indexPaciente"),
    path('cuenta/<id>',mi_cuenta,name="micuenta")
]