from array import array
from multiprocessing import context
from multiprocessing.sharedctypes import Array
from select import select
from django.shortcuts import render
from django.contrib.auth.models import User
from modulo_admin.models import Comuna, EstadoCivil, Genero, Medico, Nacionalidad, Paciente, Usuario, Atencion, Farmaco, Prevision, TelefonoUsuario, Telefono
from modulo_admin.models import TipoFarmaco, PerfilUsuario, Administrador, Recepcionista, Contrato, TipoContrato, Alergia, DetalleAlergia,DetalleAtencion
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.db.models import Count
from django.contrib import messages
import logging
from django.http import JsonResponse
import datetime
# Create your views here.


def inicio(request):
    comunas = Comuna.objects.all()
    cat_prevision = Prevision.objects.all()
    estadoCivil = EstadoCivil.objects.all()
    admin_farmaco = Farmaco.objects.all()
    ####filtro Paciente#####
    pacienteAtencion = Paciente.objects.values_list('run_paciente')
    ########################
    
    pacientes = Usuario.objects.filter(id_perfil = 4)[:10]
    nacionalidades = Nacionalidad.objects.all()

    contexto = {"prevision": cat_prevision,
                "ECivil": estadoCivil, 
                "comunas": comunas,
                "via_admin": admin_farmaco,
                "nacionalidad": nacionalidades,
                "pacientes": pacientes,
                "runPaciente": pacienteAtencion,
                "nacionalidad": nacionalidades,
                }

    return render(request,"base_medico.html", contexto)

def agenda(request):
    array_paciente=[]
    array_antiguedad=[]
    pacientes = Usuario.objects.filter(id_perfil = 4)[:20]
    for x in pacientes:
        array_paciente.append(x.run)
    for x in array_paciente:
        ateExiste = DetalleAtencion.objects.filter(run_paciente=x)
        cant = ateExiste.count()
        if cant > 0:
            array_antiguedad.append("Antiguo")          
        else:
            array_antiguedad.append("Nuevo")
    zip(pacientes,array_antiguedad)
    contexto = {
        "pacientes":pacientes,
        "antiguo":zip(pacientes,array_antiguedad),
    }
    return render(request,"agenda_paciente.html",contexto)

def atePaciente(request,id):

    tel_users = TelefonoUsuario.objects.get(run_usuario=id)
    usuario = Usuario.objects.get(run=id)
    pacientePrev = Paciente.objects.get(run_paciente = id)
    comunas = Comuna.objects.all()
    cat_prevision = Prevision.objects.all()
    estadoCivil = EstadoCivil.objects.all()
    nacionalidades = Nacionalidad.objects.all()
    atencion = DetalleAtencion.objects.filter(run_paciente=id)


    if request.POST:        

        talla = request.POST.get("inputTalla")
        peso = request.POST.get("inputPeso")
        imc = request.POST.get("inputIMC")
        observacion = request.POST.get("inputObservacion")
        cirugia = request.POST.get("inputHClinico")
        diagnostico = request.POST.get("inputDiagnostico")
        

        
    
    contexto = {
        "prevision": cat_prevision,
        "ECivil": estadoCivil, 
        "comunas": comunas,  
        "nacionalidad": nacionalidades,
        "paciente":usuario,
        "telePac":tel_users,
        "prevPaciente": pacientePrev
        
    }
    return render(request,"atencion_paciente.html",contexto)

def consultaV(request):
    return render(request,"consulta_paciente.html")
def consultaP(request,id):
    return render(request,"consulta_paciente.html")
def examenesP(request):
    return render(request,"examenes_paciente.html")    
