from array import array
from cProfile import run
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
from modulo_admin.models import Agenda, Comuna, Diagnostico, EstadoCivil, Genero, Medico, Nacionalidad, Paciente, ResultadoExamen, TipoDiagnostico, Usuario, Atencion, Farmaco, Prevision, TelefonoUsuario, Telefono
from modulo_admin.models import TipoFarmaco, PerfilUsuario, Administrador, Recepcionista, Contrato, TipoContrato, Alergia, DetalleAlergia, DetalleAtencion
from modulo_medico.models import Disponibilidad, agenda_hora, det_agenda
from modulo_admin.metodos import agregar_disp
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Count
from django.contrib import messages
import logging
from django.http import JsonResponse
import time
import numpy as np
import datetime
from django.db.models import Max
from django.shortcuts import redirect
from django.utils import timezone
from django.db import connection

# Create your views here.

def insert_DetAtencio(x,y):
    with connection.cursor() as cursor:
        cursor.callproc("sp_detalle_atencion", (x,y))
    return True

def inicio(request):
    return render(request, "index_medico.html")


def agenda(request):
    # objetos nuevos

    ##########
    array_paciente = []
    array_antiguedad = []
    pacientes = Usuario.objects.filter(id_perfil=4)[:20]
    for x in pacientes:
        array_paciente.append(x.run)
    for x in array_paciente:
        ateExiste = DetalleAtencion.objects.filter(run_paciente=x)
        cant = ateExiste.count()
        if cant > 0:
            array_antiguedad.append("Antiguo")
        else:
            array_antiguedad.append("Nuevo")
    zip(pacientes, array_antiguedad)

    # codigo agregado

    if request.POST:
        # RECOGE LA DISPONIBILIDAD SELECCIONADA DE HORARIO MEDICO

        d_lun = request.POST.getlist("lu")
        d_mar = request.POST.getlist("ma")
        d_mier = request.POST.getlist("mi")
        d_jue = request.POST.getlist("ju")
        d_vie = request.POST.getlist("vi")

        # SI HAY DATOS INSERTA LA DISPONIBILIDAD EN TABLA METODO EN metodos.py
        if d_lun is not None and len(d_lun) > 0:
            print(d_lun)
            agregar_disp(d_lun, 2222222)
        if d_mar is not None and len(d_mar) > 0:
            print(d_mar)
            agregar_disp(d_mar, 2222222)
        if d_mier is not None and len(d_mier) > 0:
            print(d_mier)
            agregar_disp(d_mier, 2222222)
        if d_jue is not None and len(d_jue) > 0:
            print(d_jue)
            agregar_disp(d_jue, 2222222)
        if d_vie is not None and len(d_vie) > 0:
            print(d_vie)
            agregar_disp(d_mier, 2222222)
    # RECOGE HORAS ASIGNADAS PREVIAMENTE
    disp = Disponibilidad.objects.filter(run_medico=2222222)

    ################################
    contexto = {
        "pacientes": pacientes,
        "antiguo": zip(pacientes, array_antiguedad),
        "disponibilidad": disp
    }
    return render(request, "agenda_paciente.html", contexto)


def atePaciente(request, id):

    tel_users = TelefonoUsuario.objects.get(run_usuario=id)
    usuario = Usuario.objects.get(run=id)
    pacientePrev = Paciente.objects.get(run_paciente=id)
    comunas = Comuna.objects.all()
    cat_prevision = Prevision.objects.all()
    estadoCivil = EstadoCivil.objects.all()
    nacionalidades = Nacionalidad.objects.all()
    mostrarAlergia = Alergia.objects.all()

    #id_at= list(a_pac.values_list("id_atencion"))
    id_diag = Diagnostico.objects.aggregate(maximo=Max('id_diagnostico'))['maximo'] 
    id_at = Atencion.objects.aggregate(maximo=Max('id_atencion'))['maximo']

    if request.POST:
    
        talla = request.POST.get("inputTalla")
        peso = request.POST.get("inputPeso")
        imc = request.POST.get("inputIMC")
        observacion = request.POST.get("inputObservacion")
        cirugia = request.POST.get("inputHClinico")
        diagnostico = request.POST.get("inputDiagnostico")
        medicamento = request.POST.get("inputHabmed")
        ############## Registro de Diagnostico = Z  ######################
        z = Diagnostico()
        z.id_diagnostico = id_diag+1
        z.nombre_diag = diagnostico
        z.id_tipo_diag = TipoDiagnostico.objects.get(id_tipo_diag=1)


        ################### Paciente = X ###########################
        x = Paciente()
        x.id_prevision = pacientePrev.id_prevision
        x.run_paciente = pacientePrev.run_paciente
        x.talla = talla
        x.peso = peso
        x.imc = imc
        x.observaciones = observacion
        x.cirugias = cirugia
        x.enfermedad = diagnostico
        x.medicacion_habitual = medicamento
               
        if x.talla is not None and x.peso is not None and x.imc is not None and x.observaciones is not None and x.cirugias is not None and x.enfermedad is not None and x.medicacion_habitual:
            if x.talla.strip() != '' and x.peso.strip() != '' and x.imc.strip() != '' and x.observaciones.strip() != '' and x.cirugias.strip() != '' and x.enfermedad.strip() != '' and x.medicacion_habitual:
                #try:
                    z.save()
                    
                    #### Valores Registro Atencion = Y #############################
                    y = Atencion()
                    y.id_atencion = id_at+7
                    y.id_diagnostico = Diagnostico.objects.get(id_diagnostico=z.id_diagnostico)
                    y.exploracion_clinica = observacion
                    y.comentario_atencion = "prueba 999"
                    y.tratamiento = medicamento
                    #y.id_receta = None
                    #y.id_examen = None
                    #y.id_licencia = None
                    y.id_agenda =  Agenda.objects.get(id_agenda=999)
                    x.save()
                    y.save()
                    i_a = Atencion.objects.get(id_atencion=y.id_atencion)
                    print(f'objeto atencion {y.id_atencion}---{i_a}')
                    ###### Valores Detalle Atencion ##########
                    insert_DetAtencio(id,y.id_atencion)
                     
                        #print("malo el atencion")
                                    
                #except:
                    #print("Error Prueba de REGISTRO datos PACIENTE")
            else:
                print("Error, Campos con Espacio")
        else:
            print("Error, Campos Nulos") 

    contexto = {
        "prevision": cat_prevision,
        "ECivil": estadoCivil,
        "comunas": comunas,
        "nacionalidad": nacionalidades,
        "paciente": usuario,
        "telePac": tel_users,
        "prevPaciente": pacientePrev,
        "selectAlergia": mostrarAlergia,
    }
    return render(request, "atencion_paciente.html", contexto)


def consultaV(request):
    # Estado Civil sin paciente.
    estadoCivil = EstadoCivil.objects.all()
    # Prevision sin pacientes
    cat_prevision = Prevision.objects.all()
    # Alergias sin paciente
    mostrarAlergia = Alergia.objects.all()
    # Nacionalidad Sin paciente
    nacionalidades = Nacionalidad.objects.all()
    # Comunas sin paciente.
    comunas = Comuna.objects.all()
    # Usuario para datos del paciente en general
    user = Usuario.objects.all()
    if request.POST:
        run_paciente = request.POST.get("rutPaciente2")
        user_c = Usuario.objects.all().filter(run=run_paciente).count()
        print(user_c)

        if user_c > 0:                   
            return redirect('consultaP', id=run_paciente)
        else:   
            mensaje = True
            contexto = {"ECivil": estadoCivil,
                        "prevision": cat_prevision,
                        "selectAlergia": mostrarAlergia,
                        "Nacionalidad": nacionalidades,
                        "Comunas": comunas,
                        "User_p": user,
                        "existe": mensaje
                        }
            return render(request, "consulta_paciente.html", contexto)    
    else:
        mensaje = False
        contexto = {"ECivil": estadoCivil,
                    "prevision": cat_prevision,
                    "selectAlergia": mostrarAlergia,
                    "Nacionalidad": nacionalidades,
                    "Comunas": comunas,
                    "User_p": user,
                    "existe": mensaje
                    }
        return render(request, "consulta_paciente.html", contexto)


def consultaP(request, id):
    mensaje = 0
    # Pacioente Antiguo por ID, datos de observaciones y demas
    pacientes = Paciente.objects.get(run_paciente=id)
    # Usuario para datos del paciente en general
    user = Usuario.objects.get(run=id)
    # Telefono del usuario por ID = run
    tel_users = TelefonoUsuario.objects.get(run_usuario=id)
    # atencion del paciente solo 1

    # Estado Civil sin paciente.
    estadoCivil = EstadoCivil.objects.all()
    # Prevision sin pacientes
    cat_prevision = Prevision.objects.all()
    # Alergiias sin paciente
    mostrarAlergia = Alergia.objects.all()
    # Nacionalidad Sin paciente
    nacionalidades = Nacionalidad.objects.all()
    # Comunas sin paciente.
    comunas = Comuna.objects.all()

    if request.POST:
        uPac = Paciente()
        userP = Usuario()
        tel_u = Telefono()

        #####Datos Usuario
        userP.run = user.run
        userP.dv = user.dv
        userP.p_nombre = user.p_nombre
        userP.s_nombre = user.s_nombre
        userP.apellido_pa = user.apellido_pa
        userP.apellido_ma = user.apellido_ma
        userP.id_perfil = user.id_perfil
        userP.fecha_nac = user.fecha_nac
        userP.contrasena = user.contrasena
        userP.id_genero = user.id_genero
        userP.id_nacionalidad = user.id_nacionalidad
        correo = request.POST.get("inputcorreo2")
        userP.correo = correo
        direcc = request.POST.get("inputDireccion2")
        userP.direccion = direcc
        com_p = request.POST.get("inputComuna2")
        userP.id_comuna = Comuna.objects.get(nombre_comuna=com_p)
        estado =  request.POST.get("inputEstado2")   
        userP.id_estado = EstadoCivil.objects.get(nombre_estado=estado)
        tel_u.num_telefono = tel_users.id_telefono.num_telefono
        
        ######Datos Paciente
        uPac.run_paciente = pacientes.run_paciente
        uPac.id_prevision = pacientes.id_prevision
        talla = request.POST.get("inputTalla2")
        uPac.talla = talla
        peso =  request.POST.get("inputPeso2")
        uPac.peso = peso
        imc = request.POST.get("inputIMC2")
        uPac.imc = imc
        observacion = request.POST.get("inputObservacion2")
        uPac.observaciones = observacion
        cirugia = request.POST.get("inputHClinico2")
        uPac.cirugias = cirugia
        diagnostico = request.POST.get("inputDiagnostico2")
        uPac.enfermedades = diagnostico
        medicamento = request.POST.get("inputHabmed2")
        uPac.medicacion_habitual = medicamento
        if userP.correo is not None and userP.direccion is not None and userP.id_comuna is not None and userP.id_estado is not None and uPac.talla is not None and uPac.peso is not None and uPac.observaciones is not None and uPac.cirugias is not None and uPac.enfermedades is not None and uPac.medicacion_habitual:
            if  userP.correo.strip() != '' and userP.direccion.strip() != '' and uPac.talla.strip() != '' and uPac.peso.strip() != '' and uPac.observaciones.strip() != '' and uPac.cirugias.strip() != '' and uPac.enfermedades.strip() != '' and uPac.medicacion_habitual:
                try:
                    mensaje = 0
                    uPac.save()
                    userP.save()
                    return redirect('consultaP', id=user.run)
                except:
                    mensaje= 1
            else:
                mensaje= 2
        else:
            mensaje= 3

    contexto = {"User_p": user,
                "paciente": pacientes,
                "ECivil": estadoCivil,
                "prevision": cat_prevision,
                "selectAlergia": mostrarAlergia,
                "Nacionalidad": nacionalidades,
                "Comunas": comunas,
                "telePac": tel_users,
                "validar": mensaje

                }
    return render(request, "consulta_paciente.html", contexto)


def examenesP(request):
    if request.POST:
        paciente = request.POST.get("sPaciente")
        if paciente != '':
            examenReslt_conteo = ResultadoExamen.objects.all().filter(run_paciente=paciente).count()
            e = ResultadoExamen.objects.filter(run_paciente=paciente)
            contexto = {"eRsultados_conteo": examenReslt_conteo}
        else:
            contexto = {"Presentacion": "noexiste"}
    else:
        contexto = {"Presentacion": "nada"}
    return render(request, "examenes_paciente.html", contexto)
