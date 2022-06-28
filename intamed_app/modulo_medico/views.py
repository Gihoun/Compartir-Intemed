from array import array
from curses import use_default_colors
from email import message_from_binary_file
from multiprocessing import context
from multiprocessing.sharedctypes import Array
from pickle import NONE
from re import A
from select import select
from xml.dom import NoDataAllowedErr
from django.shortcuts import render
from django.contrib.auth.models import User
from modulo_admin.models import Comuna, EstadoCivil, Genero, Medico, Nacionalidad, Paciente, ResultadoExamen, Usuario, Atencion, Farmaco, Prevision, TelefonoUsuario, Telefono
from modulo_admin.models import TipoFarmaco, PerfilUsuario, Administrador, Recepcionista, Contrato, TipoContrato, Alergia, DetalleAlergia,DetalleAtencion
from modulo_medico.models import *
from modulo_admin.metodos import agregar_disp
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.db.models import Count
from django.contrib import messages
import logging
from django.http import JsonResponse
from datetime import datetime
import numpy as np 

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
    ### objetos nuevos
    
    ##########
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

    ################################# codigo agregado
   

    if request.POST:
        #RECOGE LA DISPONIBILIDAD SELECCIONADA DE HORARIO MEDICO
        
        d_lun = request.POST.getlist("lu")
        d_mar = request.POST.getlist("ma")
        d_mier = request.POST.getlist("mi")
        d_jue = request.POST.getlist("ju")
        d_vie = request.POST.getlist("vi")
                    
         
        #SI HAY DATOS INSERTA LA DISPONIBILIDAD EN TABLA METODO EN metodos.py
        if d_lun is not None and len(d_lun)>0:
            print(d_lun)
            agregar_disp(d_lun, 2222222)
        if d_mar is not None and len(d_mar)>0:
            print(d_mar)
            agregar_disp(d_mar, 2222222)
        if d_mier is not None and len(d_mier)>0:
            print(d_mier)
            agregar_disp(d_mier, 2222222)
        if d_jue is not None and len(d_jue)>0:
            print(d_jue)
            agregar_disp(d_jue, 2222222)
        if d_vie is not None and len(d_vie)>0:
            print(d_vie)
            agregar_disp(d_mier, 2222222)           
    # RECOGE HORAS ASIGNADAS PREVIAMENTE
    disp = Disponibilidad.objects.filter(run_medico=2222222)


    ################################
    contexto = {
        "pacientes":pacientes,
        "antiguo":zip(pacientes,array_antiguedad),
        "disponibilidad": disp
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
    mostrarAlergia = Alergia.objects.all()
    alergiaPac = DetalleAlergia.objects.filter(run_paciente = id)    
    
    if request.POST:        
        userPaciente = Paciente()
        
        userPaciente.id_prevision = pacientePrev.id_prevision
        userPaciente.run_paciente = usuario
        
        #### valores de input para paciente##

        talla = request.POST.get("inputTalla")
        userPaciente.talla = talla
        peso = request.POST.get("inputPeso")
        userPaciente.peso = peso
        imc = request.POST.get("inputIMC")
        userPaciente.imc = imc
        observacion = request.POST.get("inputObservacion")
        userPaciente.observaciones = observacion
        cirugia = request.POST.get("inputHClinico")
        userPaciente.cirugias = cirugia
        diagnostico = request.POST.get("inputDiagnostico")
        userPaciente.enfermedad = diagnostico
        medicamento = request.POST.get("inputHabmed")
        userPaciente.medicacion_habitual = medicamento


        if userPaciente.talla is not None and userPaciente.peso is not None and userPaciente.imc is not None and userPaciente.observaciones is not None and userPaciente.cirugias is not None and userPaciente.enfermedad is not None and userPaciente.medicacion_habitual:
            if userPaciente.talla.strip() !='' and userPaciente.peso.strip() !='' and userPaciente.imc.strip() !='' and userPaciente.observaciones.strip() !='' and userPaciente.cirugias.strip() !='' and userPaciente.enfermedad.strip() !='' and userPaciente.medicacion_habitual:
                try:          
                    userPaciente.save()
                except:
                    print("Error Prueba de REGISTRO datos PACIENTE")
            else:
                print("Error, Campos con Espacio")
        else:
                print("Error, Campos Nulos")        
 

    contexto = {
        "prevision": cat_prevision,
        "ECivil": estadoCivil, 
        "comunas": comunas,  
        "nacionalidad": nacionalidades,
        "paciente":usuario,
        "telePac":tel_users,
        "prevPaciente": pacientePrev,
        "selectAlergia": mostrarAlergia,
    }
    return render(request,"atencion_paciente.html",contexto)

def consultaV(request):
    
    pacientes = Paciente.objects.all() 

    return render(request,"consulta_paciente.html")
def consultaP(request,id):

    return render(request,"consulta_paciente.html")
def examenesP(request):

    if request.POST:
        paciente = request.POST.get("sPaciente")
        user  = Usuario.objects.get(run=paciente)
        print(user)
        if paciente != '':  
            examenReslt_conteo = ResultadoExamen.objects.all().filter(run_paciente=paciente).count() 
            e = ResultadoExamen.objects.filter(run_paciente=paciente)
            

            contexto = {"eRsultados_conteo":examenReslt_conteo}

        else:
            userv = Usuario.objects.get(run=12101765)
            print(userv)
            contexto = {"Presentacion":"noexiste"}

    else:
        contexto = {"Presentacion":"nada"}

    return render(request,"examenes_paciente.html",contexto)    
