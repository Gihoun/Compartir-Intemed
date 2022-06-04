from multiprocessing import context
from multiprocessing.sharedctypes import Array
from select import select
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Comuna, EstadoCivil, Genero, Medico, Nacionalidad, Paciente, Usuario, Atencion, Farmaco, Prevision, TelefonoUsuario, Telefono
from .models import TipoFarmaco, PerfilUsuario, Administrador, Recepcionista, Contrato, TipoContrato, Alergia, DetalleAlergia
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required,permission_required
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.db.models import Count
from django.contrib import messages
import logging
from django.http import JsonResponse
import datetime
# Create your views here.

def inicio(request):
    user= Medico.Object.all()
    return render(request,"base_medico.html")

  

def prueba(request):
    return render(request,"contenido_medico.html")