from django.contrib import admin
from django.urls import path
from .views import inicio, micuenta, nuestraclinica, funcionarios

urlpatterns = [   
    path('inicio/',inicio,name="index"),
    path('micuenta/',micuenta,name="micuenta"),
    path('nuestraclinica/',nuestraclinica,name="nuestraclinica"),
    path('funcionarios/',funcionarios,name="funcionarios"),
]