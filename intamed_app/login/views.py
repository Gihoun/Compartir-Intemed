from django.shortcuts import render
from modulo_admin.models import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required,permission_required
import requests


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
            userL = request.user.username
        else:
            
            mensaje="No existe usuario o contrasennia incorrecta si desea activar cuenta presione ok"
    contexto = {"uname": userL,"mensaje":mensaje}
   
    return render(request,'base_login.html', contexto )
def activar_cuenta(request):


    if request.POST:

        user = User.objects.create_user(username='john',
                                        email='jlennon@beatles.com',
                                        password='glass onion')