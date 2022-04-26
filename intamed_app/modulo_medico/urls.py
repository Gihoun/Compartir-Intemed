from django.contrib import admin
from django.urls import path
from .views import inicio, administrator

urlpatterns = [   
    path('inicio/',inicio,name="index"),
    path('administracion/',administrator,name="administracion"),
]