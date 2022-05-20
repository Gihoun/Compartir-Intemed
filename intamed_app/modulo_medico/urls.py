from django.contrib import admin
from django.urls import path
from .views import inicio, prueba

urlpatterns = [   
    path('inicio/',inicio,name="index"),
    path('testeo/',prueba,name="test"),
]