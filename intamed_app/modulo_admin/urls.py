from django.contrib import admin
from django.urls import path
from .views import administrator

urlpatterns = [   
    path('administracion/',administrator,name="administracion"),
]