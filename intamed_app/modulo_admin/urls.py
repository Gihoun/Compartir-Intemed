from django.contrib import admin
from django.urls import path
from .views import administrator, filtro_usuarios

urlpatterns = [   
    path('panel/',administrator,name="Dash"),
    path('panel/userg',filtro_usuarios,name="userg"),
]