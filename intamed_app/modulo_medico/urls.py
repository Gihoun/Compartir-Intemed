from django.contrib import admin
from django.urls import path
from .views import inicio

urlpatterns = [   
    path('inicio/',inicio,name="index"),
]