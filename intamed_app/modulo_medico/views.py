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
from modulo_admin.models import Agenda, Comuna, DetalleFarmaco, Diagnostico, EstadoCivil, Genero, Medico, Nacionalidad, Paciente, Receta, ResultadoExamen, TipoDiagnostico, Usuario, Atencion, Farmaco, Prevision, TelefonoUsuario, Telefono
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
import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

# Create your views here.


def insert_DetAtencio(x, y):
    with connection.cursor() as cursor:
        cursor.callproc("sp_detalle_atencion", (x, y))
    return True


def insert_DetFarmaco(x, y):
    with connection.cursor() as cursor:
        cursor.callproc("sp_detalle_farmaco", (x, y))
    return True


def inicio(request):

    logueado = request.user
    run_med = logueado.usuario_django.run_django
    usu_medico = Usuario.objects.get(run=run_med)
    contexto = {"medico": usu_medico}
    return render(request, "index_medico.html", contexto)


def agenda(request):
    # obtiene el medico autenticado
    logueado = request.user
    run_med = logueado.usuario_django.run_django
    usu_medico = Usuario.objects.get(run=run_med)
    print(f'este es el usuario django en agenda {run_med}')
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
            agregar_disp(d_lun, run_med)
        if d_mar is not None and len(d_mar) > 0:
            print(d_mar)
            agregar_disp(d_mar, run_med)
        if d_mier is not None and len(d_mier) > 0:
            print(d_mier)
            agregar_disp(d_mier, run_med)
        if d_jue is not None and len(d_jue) > 0:
            print(d_jue)
            agregar_disp(d_jue, run_med)
        if d_vie is not None and len(d_vie) > 0:
            print(d_vie)
            agregar_disp(d_mier, run_med)
    # RECOGE HORAS ASIGNADAS PREVIAMENTE
    disp = Disponibilidad.objects.filter(run_medico=run_med)

    ################################
    contexto = {
        "pacientes": pacientes,
        "antiguo": zip(pacientes, array_antiguedad),
        "disponibilidad": disp,
        "medico": usu_medico
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
    farma = Farmaco.objects.all()
    t_diag = TipoDiagnostico.objects.all()
    t_farma = TipoFarmaco.objects.all()
    id_diag = Diagnostico.objects.aggregate(
        maximo=Max('id_diagnostico'))['maximo']
    id_at = Atencion.objects.aggregate(maximo=Max('id_atencion'))['maximo']
    id_receta = Receta.objects.aggregate(maximo=Max('id_receta'))['maximo']

    if request.POST:

        # VAR de Usuario para su modificacion
        correo = request.POST.get("inputcorreo")
        fono = request.POST.get("inputFono")
        nacionaldiad = request.POST.get("inpucNac")
        direccion = request.POST.get("inputDireccion")
        comuna = request.POST.get("inputComuna")

        # Var de Paciente para su modificacion
        talla = request.POST.get("inputTalla")
        peso = request.POST.get("inputPeso")
        imc = request.POST.get("inputIMC")
        observacion = request.POST.get("inputObservacion")
        cirugia = request.POST.get("inputHClinico")
        diagnostico = request.POST.get("inputDiagnostico")
        medicamento = request.POST.get("inputHabmed")

        # var de tipo de diagnostico
        t_diagnostico = request.POST.get("inputDiag")

        ## Var de Farmacos para la medicacion habitual solo para los informes #####
        farmaname = request.POST.getlist('inputNfarmaco')
        farmadosis = request.POST.getlist('inputDfarmaco')
        farmaadmin = request.POST.getlist('inputVfarmaco')
        farmatipo = request.POST.getlist('inputTfarmaco')

        ############## Registro de Diagnostico = Z  ######################

        z = Diagnostico()
        z.id_diagnostico = id_diag+1
        z.nombre_diag = diagnostico
        z.id_tipo_diag = TipoDiagnostico.objects.get(tipo_diag=t_diagnostico)

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

        ################## Receta Paciente = R ##################################
        r = Receta()
        r.id_receta = id_receta + 1
        r.descripcion_receta = medicamento

        if x.talla is not None and x.peso is not None and x.imc is not None and x.observaciones is not None and x.cirugias is not None and x.enfermedad is not None and x.medicacion_habitual:
            if x.talla.strip() != '' and x.peso.strip() != '' and x.imc.strip() != '' and x.observaciones.strip() != '' and x.cirugias.strip() != '' and x.enfermedad.strip() != '' and x.medicacion_habitual:
                try:
                    z.save()
                    r.save()
                    ################### Detalle Farmaco = dt ####################################
                    for f in farmaname:
                        fa = Farmaco.objects.get(nombre_farmaco=f)
                        insert_DetFarmaco(r.id_receta, fa.id_farmaco)
                    #### Valores Registro Atencion = Y #############################
                    y = Atencion()
                    y.id_atencion = id_at+7
                    y.id_diagnostico = Diagnostico.objects.get(
                        id_diagnostico=z.id_diagnostico)
                    y.exploracion_clinica = observacion
                    if r.id_receta is not None:
                        y.id_receta = Receta.objects.get(id_receta=r.id_receta)
                    else:
                        y.id_receta = None
                    y.comentario_atencion = "prueba 999"
                    y.tratamiento = medicamento
                    y.id_agenda = Agenda.objects.get(id_agenda=999)
                    x.save()
                    y.save()

                    ###### Valores Detalle Atencion ##########
                    insert_DetAtencio(id, y.id_atencion)
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
        "paciente": usuario,
        "telePac": tel_users,
        "prevPaciente": pacientePrev,
        "selectAlergia": mostrarAlergia,
        "tip_diag": t_diag,
        "todo_farma": farma,
        "tip_farma": t_farma

    }
    return render(request, "atencion_paciente.html", contexto)


def some_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


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
    # BUSCAR MANERA DE TRAER EL OBJETO MEDICO USER AUTHENTICATED

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

    farma = Farmaco.objects.all()
    t_diag = TipoDiagnostico.objects.all()
    id_diag = Diagnostico.objects.aggregate(
        maximo=Max('id_diagnostico'))['maximo']
    id_at = Atencion.objects.aggregate(maximo=Max('id_atencion'))['maximo']
    t_farma = TipoFarmaco.objects.all()
    id_receta = Receta.objects.aggregate(maximo=Max('id_receta'))['maximo']

    if request.POST:
        x = Paciente()
        u = Usuario()
        tel_u = Telefono()

        # Datos Usuario
        u.run = user.run
        u.dv = user.dv
        u.p_nombre = user.p_nombre
        u.s_nombre = user.s_nombre
        u.apellido_pa = user.apellido_pa
        u.apellido_ma = user.apellido_ma
        u.id_perfil = user.id_perfil
        u.fecha_nac = user.fecha_nac
        u.contrasena = user.contrasena
        u.id_genero = user.id_genero
        u.id_nacionalidad = user.id_nacionalidad
        correo = request.POST.get("inputcorreo2")
        u.correo = correo
        direcc = request.POST.get("inputDireccion2")
        u.direccion = direcc
        com_p = request.POST.get("inputComuna2")
        u.id_comuna = Comuna.objects.get(nombre_comuna=com_p)
        estado = request.POST.get("inputEstado2")
        u.id_estado = EstadoCivil.objects.get(nombre_estado=estado)
        tel_u.num_telefono = tel_users.id_telefono.num_telefono

        # Datos Paciente
        x.run_paciente = pacientes.run_paciente
        x.id_prevision = pacientes.id_prevision
        talla = request.POST.get("inputTalla2")
        x.talla = talla
        peso = request.POST.get("inputPeso2")
        x.peso = peso
        imc = request.POST.get("inputIMC2")
        x.imc = imc
        observacion = request.POST.get("inputObservacion2")
        x.observaciones = observacion
        cirugia = request.POST.get("inputHClinico2")
        x.cirugias = cirugia
        diagnostico = request.POST.get("inputDiagnostico2")
        x.enfermedades = diagnostico
        medicamento = request.POST.get("inputHabmed")
        x.medicacion_habitual = medicamento

        # var de tipo de diagnostico
        t_diagnostico = request.POST.get("inputDiag")

        ## Var de Farmacos para la medicacion habitual solo para los informes #####
        farmaname = request.POST.getlist('inputNfarmaco')
        farmadosis = request.POST.getlist('inputDfarmaco')
        farmaadmin = request.POST.getlist('inputVfarmaco')
        farmatipo = request.POST.getlist('inputTfarmaco')

        ############## Registro de Diagnostico = Z  ######################

        z = Diagnostico()
        z.id_diagnostico = id_diag+1
        z.nombre_diag = diagnostico
        z.id_tipo_diag = TipoDiagnostico.objects.get(tipo_diag=t_diagnostico)

        ################## Receta Paciente = R ##################################
        r = Receta()
        r.id_receta = id_receta + 1
        r.descripcion_receta = medicamento

        if u.correo is not None and u.direccion is not None and u.id_comuna is not None and u.id_estado is not None and x.talla is not None and x.peso is not None and x.observaciones is not None and x.cirugias is not None and x.enfermedades is not None and x.medicacion_habitual:
            if u.correo.strip() != '' and u.direccion.strip() != '' and x.talla.strip() != '' and x.peso.strip() != '' and x.observaciones.strip() != '' and x.cirugias.strip() != '' and x.enfermedades.strip() != '' and x.medicacion_habitual:
                try:
                    mensaje = 0
                    z.save()
                    r.save()
                    ################### Detalle Farmaco = dt ####################################
                    for f in farmaname:
                        fa = Farmaco.objects.get(nombre_farmaco=f)
                        insert_DetFarmaco(r.id_receta, fa.id_farmaco)
                    #### Valores Registro Atencion = Y #############################
                    y = Atencion()
                    y.id_atencion = id_at+7
                    y.id_diagnostico = Diagnostico.objects.get(id_diagnostico=z.id_diagnostico)
                    y.exploracion_clinica = observacion
                    if r.id_receta is not None:
                        y.id_receta = Receta.objects.get(id_receta=r.id_receta)
                    else:
                        y.id_receta = None
                    y.comentario_atencion = "prueba 999"
                    y.tratamiento = medicamento
                    y.id_agenda = Agenda.objects.get(id_agenda=999)

                    u.save()
                    x.save()
                    y.save()

                    ###### Valores Detalle Atencion ##########
                    insert_DetAtencio(id, y.id_atencion)
                    #return redirect('consultaP', id=user.run)
                except:
                    mensaje = 1
            else:
                mensaje = 2
        else:
            mensaje = 3

    contexto = {"User_p": user,
                "paciente": pacientes,
                "ECivil": estadoCivil,
                "prevision": cat_prevision,
                "selectAlergia": mostrarAlergia,
                "Nacionalidad": nacionalidades,
                "Comunas": comunas,
                "telePac": tel_users,
                "validar": mensaje,
                "tip_diag": t_diag,
                "todo_farma": farma,
                "tip_farma": t_farma
                }
    return render(request, "consulta_paciente.html", contexto)


def examenesP(request):
    if request.POST:
        paciente = request.POST.get("sPaciente")
        if paciente != '':
            examenReslt_conteo = ResultadoExamen.objects.all().filter(
                run_paciente=paciente).count()
            e = ResultadoExamen.objects.filter(run_paciente=paciente)
            contexto = {"eRsultados_conteo": examenReslt_conteo}
        else:
            contexto = {"Presentacion": "noexiste"}
    else:
        contexto = {"Presentacion": "nada"}
    return render(request, "examenes_paciente.html", contexto)
