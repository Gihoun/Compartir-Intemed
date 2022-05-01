from django.contrib import admin
from django.urls import path
from .views import inicio, micuenta, nuestraclinica

urlpatterns = [   
    path('inicio/',inicio,name="index"),
    path('micuenta/',micuenta,name="index"),
    path('nuestraclinica/',nuestraclinica,name="index"),
]