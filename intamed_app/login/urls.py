from django.contrib import admin
from django.urls import path
from .views import login_todos

urlpatterns = [  
    path('',login_todos, name="login"), 
    #path('colab/',inicio, name="logincol"),
    #path('paciente/',buscarPaciente, name="loginPac")
]