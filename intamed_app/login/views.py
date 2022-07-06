from django.shortcuts import render
from modulo_admin.models import *
from modulo_paciente.views import *
from .models import Usuario_django
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import redirect
import requests
from select import select

# Create your views here.

def login_todos(request):
    mensaje= ""
    userL = ''
    contexto = {}
    
    if request.POST:
        nombre = request.POST.get("nameU")
        passwd = request.POST.get("passwd")
        print(nombre)
        print(passwd)
        us = authenticate(request,username=nombre,password=passwd)
        if us is not None and us.is_active:
            login(request, us)
            userDJ = User.objects.get(username=nombre)
            ru = userDJ.usuario_django.run_django
            userORA = Usuario.objects.get(run=ru)
            perf = userORA.id_perfil_id
            
            print(f"perfil {perf}")
            if perf == 4:#Medico
                med = Usuario.objects.filter(id_perfil=2)
                contexto ={"paciente": userORA,"medico":med}
                response = redirect('modulo_paciente:indexPaciente',id=userORA.run)
                return response
                #return render(request, 'paciente.html', contexto )
            elif perf == 1:##Admin
                contexto ={"admin": userORA}
                return render(request, 'administrator.html', contexto )
            elif perf==2:##Medico
                response = redirect('modulo_medico:index')
                return response

        else:
            
            mensaje="No existe usuario o contrasennia incorrecta"
    contexto = {"uname": userL,"mensaje":mensaje}
   
    return render(request,'base_login.html', contexto)

def activar_cuenta(request):
    if request.POST:
        user = User.objects.create_user(username='john',
                                        email='jlennon@beatles.com',
                                        password='glass onion')