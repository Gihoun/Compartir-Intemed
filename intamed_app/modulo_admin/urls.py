from django.contrib import admin
from django.urls import path
from .views import administrator, filtro_usuarios, vista_farmaco

urlpatterns = [   
    path('panel/',administrator,name="Dash"),
    path('panel/userg',filtro_usuarios,name="userg"),
    path('panel/farmaco',vista_farmaco,name="farmag")
]