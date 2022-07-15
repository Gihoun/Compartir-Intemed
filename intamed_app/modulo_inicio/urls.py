from django.contrib import admin
from django.urls import path
from .views import  micuenta, nuestraclinica

urlpatterns = [      
    path('micuenta/<id>',micuenta,name="micuenta"),
    path('nuestraclinica/',nuestraclinica,name="nuestraclinica"),

]