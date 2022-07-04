from django.contrib import admin
from django.urls import path
from .views import login_todos
from modulo_paciente.views import *

urlpatterns = [  
    path('',login_todos, name="login"), 
    path('',login_todos, name="index"),
]