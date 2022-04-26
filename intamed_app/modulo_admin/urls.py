from django.contrib import admin
from django.urls import path
from .views import administrator

urlpatterns = [   
    path('panel/',administrator,name="administracion"),
]