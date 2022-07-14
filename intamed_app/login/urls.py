from django.contrib import admin
from django.urls import path
from .views import login_todos, log_out
from modulo_paciente.views import *


urlpatterns = [  
    path('',login_todos, name="login"), 
    path('',login_todos, name="index"),
    path('logout',log_out, name="logout"),
]