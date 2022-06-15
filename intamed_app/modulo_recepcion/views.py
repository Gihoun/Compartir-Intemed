from multiprocessing.sharedctypes import Array
from select import select
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Comuna, EstadoCivil, Genero, Medico, Nacionalidad, Paciente, Usuario, Atencion, Farmaco
from .models import TipoFarmaco, PerfilUsuario, Administrador, Recepcionista, Contrato, TipoContrato, Alergia
from .models import Prevision, TelefonoUsuario, Telefono, DetalleAlergia
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required,permission_required
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.db.models import Count
from django.contrib import messages
import requests
import logging
from django.http import JsonResponse
import datetime

from django.http import HttpRequest

# Create your views here.

def inicio(request):
    comunas = Comuna.objects.all()
    estado = EstadoCivil.objects.all()
    generos = Genero.objects.all()
    nacionalidades = Nacionalidad.objects.all()
    paciente = Usuario.objects.filter()


    contexto = {"estadoCivil":estado, "comuna":comunas, "genero": generos, "nacionalidad": nacionalidades}
    return render(request,"ingresar_paciente.html",contexto)


def buscarPaciente(request):
    return render(request,"buscar_paciente.html")

def ingresarPago(request):
    return render(request,"ingresar_pago.html")

