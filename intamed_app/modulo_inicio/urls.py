from django.contrib import admin
from django.urls import path
from .views import  micuenta, nuestraclinica, funcionarios

urlpatterns = [      
    path('micuenta/',micuenta,name="micuenta"),
    path('nuestraclinica/',nuestraclinica,name="nuestraclinica"),
    path('funcionarios/',funcionarios,name="funcionarios"),
]