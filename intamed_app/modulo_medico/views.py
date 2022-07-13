from array import array
from cProfile import run
from cmath import exp
from curses import use_default_colors
from email import message_from_binary_file
from multiprocessing import context
from multiprocessing.sharedctypes import Array
from pickle import NONE
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
from reportlab.pdfgen import canvas
from django.http import FileResponse
from reportlab.lib.pagesizes import letter

# Create your views here.

def insert_DetAtencio(x, y):
    with connection.cursor() as cursor:
        cursor.callproc("sp_detalle_atencion", (x, y))
    return True


def insert_DetFarmaco(x, y):
    with connection.cursor() as cursor:
        cursor.callproc("sp_detalle_farmaco", (x, y))
    return True

def receta_test(request,ate,id,id_r):
    
    ## id ppara personalizar
    ar_id = id.split('-')
    u =  Usuario.objects.get(run = ar_id[1])
    a = Atencion.objects.get(id_atencion = ar_id[0])
    fecha = a.fecha_atencion
    formato = fecha.strftime("%d - %m - %Y")
    
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    p.drawString(220, 800, f"Receta Médica")
    p.drawString(20, 780, f"Nombre Paciente : {u.p_nombre} {u.s_nombre} {u.apellido_pa} {u.apellido_ma}")
    p.drawString(350, 780, f"Folio receta: re00{id_r}")
    p.drawString(20, 760, f"Edad                  : {u.edad_actual} años")
    p.drawString(350, 760, f"Sexo: {u.id_genero.nombre_genero}")

    p.drawString(20, 740, f"Direccion           : {u.direccion}")
    p.drawString(20, 720, f"Fecha Emisión  :  {formato} ")
    p.drawString(350,740, f"Direccion clinica: [Direccion Clinica X, X] ")
    
    p.line(20,700,570,700)
    p.drawString(20, 680, f"Descripción de la receta: ")
    p.drawString(40, 620, ate)
    p.line(20, 120, 570, 120)
    
    p.drawString(350, 100, f"Run profesional : ")
    p.drawString(350, 80, f"Medico Tratante : ")
    p.drawString(350, 60, f"Especialidad    : ")
    p.drawString(20, 100, f"Servicios de salud Intemed ")
    p.drawString(20, 80, f"RUT: 96.999.888-2 ")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    namefile = 'Re'+str(id)+'ta-'+str(id_r)+'.pdf'
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=namefile)

def insert_DetAlergia(x, y):
    with connection.cursor() as cursor:
        cursor.callproc("sp_detalle_alergia", (x, y))
    return True

def receta_med(request,id):  
    ar_id = id.split('-')
    u =  Usuario.objects.get(run = ar_id[1])
    a = Atencion.objects.get(id_atencion = ar_id[0])
    id_re = Receta.objects.aggregate(maximo=Max('id_receta'))['maximo']
    if request.POST:
        det_R = request.POST.get("recetaP")
        if det_R is not None:
            if det_R.strip() != '':        
                try:
                    r = Receta()       
                    r.id_receta = id_re + 1
                    r.descripcion_receta = det_R
                    r.save()
                    return receta_test(request,det_R,id,r.id_receta)

                except:
                    er = 1
                    print('mal')
            else:
                print('mal srp')
                er= 2

    
    contexto = {
        "user":u,
        "atencion":a,
        "id":id
    }
    return render(request,"med_receta.html",contexto)


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
        if cant > 1:
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
            agregar_disp(d_vie, run_med)
    # RECOGE HORAS ASIGNADAS PREVIAMENTE
    #medi = Medico.objects.get(run_medico=usu_medico)
    disp = Disponibilidad.objects.filter(run_medico=run_med)
    det_age= det_agenda.objects.filter(idd__in=disp)
    ################################
    contexto = {
        "pacientes": pacientes,
        "antiguo": zip(pacientes, array_antiguedad),
        "disponibilidad": disp,
        "medico": usu_medico,
        "agenda": det_age
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
    list_ate=[]
    last_detAt = DetalleAtencion.objects.filter(run_paciente=id)
    ids_ate = list(last_detAt.values_list("id_atencion"))
    for id in ids_ate:
        list_ate.append(id[0])
    try:
        aten_pa = Atencion.objects.get(id_atencion__in=list_ate)
        print(aten_pa.id_atencion)
    except:
        aten_pa= None
    
    
    
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
        enfermedad = request.POST.get("inputEnf")
        observa = request.POST.get("inputObserva")
        cirugia = request.POST.get("inputAQuiru")
        medi_hab = request.POST.get("inputHabmed")


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
        z.nombre_diag = request.POST.get("inputDiagnostico")
        z.id_tipo_diag = TipoDiagnostico.objects.get(tipo_diag=t_diagnostico)

        ################### Paciente = X ###########################
        x = Paciente()
        x.id_prevision = pacientePrev.id_prevision
        x.run_paciente = pacientePrev.run_paciente
        x.talla = talla
        x.peso = peso
        x.imc = imc
        x.observaciones = observa
        x.cirugias = cirugia
        x.enfermedades = enfermedad
        x.medicacion_habitual = medi_hab

        ################## Receta Paciente = R ##################################
        r = Receta()
        r.id_receta = id_receta + 1
        r.descripcion_receta = medi_hab

        ################## Receta Paciente = A ##################################
        a_get = request.POST.get('inputDetalleA')
        # Alergias cortadas para su identificacion
        split_ale = a_get.split()

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
                    aten_pa.id_diagnostico = Diagnostico.objects.get(id_diagnostico=z.id_diagnostico)
                    aten_pa.exploracion_clinica = request.POST.get("inputExplo")
                    if r.id_receta is not None:
                        aten_pa.id_receta = Receta.objects.get(id_receta=r.id_receta)
                    else:
                        aten_pa.id_receta = None
                    aten_pa.comentario_atencion =  request.POST.get("inputComent")
                    aten_pa.tratamiento = request.POST.get("inputTrata")
                    aten_pa.id_agenda = Agenda.objects.get(id_agenda=999)
                    x.save()
                    aten_pa.save()
                    ########## Valores de Alergias y Detalles #########
                    for a in split_ale:
                        al = Alergia.objects.get(nombre_alergia=a)
                        insert_DetAlergia(id, al.id_alergia)
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
        "tip_farma": t_farma,
        "atencion": aten_pa

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

    t_diag = TipoDiagnostico.objects.all()
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
                        "existe": mensaje,
                        "tip_diag": t_diag,
                        }
            return render(request, "consulta_paciente.html", contexto)
    else:
        prueba = request.POST.get('inputHabmed')
        print(prueba)
        mensaje = False
        contexto = {"ECivil": estadoCivil,
                    "prevision": cat_prevision,
                    "selectAlergia": mostrarAlergia,
                    "Nacionalidad": nacionalidades,
                    "Comunas": comunas,
                    "User_p": user,
                    "existe": mensaje,
                    "tip_diag": t_diag,
                    "prueba":prueba

                    }
        return render(request, "consulta_paciente.html", contexto)


def consultaP(request, id):
    mensaje = 10
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
    # busca los farmacos del paciente.
    lista_ate = []
    far_pa = DetalleAtencion.objects.filter(run_paciente=id)
    ids_ate = list(far_pa.values_list("id_atencion"))
    for p in ids_ate:
        lista_ate.append(p[0])  
    lista_ate.sort(reverse=True)
    id_ate = Atencion.objects.get(id_atencion=lista_ate[0])
    aten_pa = Atencion.objects.filter(id_atencion__in=lista_ate).order_by('-id_atencion')[:3]
    c_receta= str(id_ate.id_atencion)+'-'+str(user.run)

    print(c_receta) 
    ids_re = []
    for rece in aten_pa:
        ids_re.append(rece.id_receta)

    far_re = DetalleFarmaco.objects.filter(id_receta__in=ids_re)
    ids_far = list(far_re.values_list("id_farmaco"))


    lista_far = []
    for h in ids_far:
        lista_far.append(h[0])
    real_far = Farmaco.objects.filter(id_farmaco__in=lista_far)

    

    farma = Farmaco.objects.all()
    t_diag = TipoDiagnostico.objects.all()
    id_diag = Diagnostico.objects.aggregate(maximo=Max('id_diagnostico'))['maximo']
    t_farma = TipoFarmaco.objects.all()
    id_receta = Receta.objects.aggregate(maximo=Max('id_receta'))['maximo']

    if request.POST:
        x = Paciente()

        tel_u = Telefono()

        # Datos Usuario

        correo = request.POST.get("inputcorreo2")
        user.correo = correo
        direcc = request.POST.get("inputDireccion2")
        user.direccion = direcc
        com_p = request.POST.get("inputComuna2")
        user.id_comuna = Comuna.objects.get(nombre_comuna=com_p)
        estado = request.POST.get("inputEstado2")
        user.id_estado = EstadoCivil.objects.get(nombre_estado=estado)
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
        observacion = request.POST.get("inputObserva")
        x.observaciones = observacion
        cirugia = request.POST.get("inputAQuiru")
        x.cirugias = cirugia
        enfer = request.POST.get("inputEnf")
        x.enfermedades = enfer
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
        z.nombre_diag = request.POST.get("inputDiagnostico2")
        z.id_tipo_diag = TipoDiagnostico.objects.get(tipo_diag=t_diagnostico)

        ################## Receta Paciente = R ##################################
        r = Receta()
        r.id_receta = id_receta + 1
        r.descripcion_receta = medicamento

        ################## Receta Paciente = A ##################################
        a_get = request.POST.get('inputDetalleA')
        # Alergias cortadas para su identificacion
        split_ale = a_get.split()

        if user.correo is not None and user.direccion is not None and user.id_comuna is not None and user.id_estado is not None and x.talla is not None and x.peso is not None and x.observaciones is not None and x.cirugias is not None and x.enfermedades is not None and x.medicacion_habitual:
            if user.correo.strip() != '' and user.direccion.strip() != '' and x.talla.strip() != '' and x.peso.strip() != '' and x.observaciones.strip() != '' and x.cirugias.strip() != '' and x.enfermedades.strip() != '' and x.medicacion_habitual:
                try:
                    z.save()
                    r.save()
                    ################### Detalle Farmaco = dt ####################################
                    for f in farmaname:
                        fa = Farmaco.objects.get(nombre_farmaco=f)
                        insert_DetFarmaco(r.id_receta, fa.id_farmaco)
                    #### Valores Registro Atencion = Y #############################
 
                    id_ate.id_diagnostico = Diagnostico.objects.get(id_diagnostico=z.id_diagnostico)
                    id_ate.exploracion_clinica = request.POST.get("inputExplo")
                    if r.id_receta is not None:
                        id_ate.id_receta = Receta.objects.get(id_receta=r.id_receta)
                    else:
                        id_ate.id_receta = None
                    ########## Valores de Alergias y Detalles #########
                    for a in split_ale:
                        al = Alergia.objects.get(nombre_alergia=a)
                        insert_DetAlergia(id, al.id_alergia)
                    id_ate.comentario_atencion = request.POST.get("inputcoment2")
                    id_ate.tratamiento = request.POST.get("inputtrata2")
                    id_ate.id_agenda = Agenda.objects.get(id_agenda=999)

                    user.save()
                    x.save()
                    id_ate.save()
                    mensaje = 0
                    return redirect('consultaP', h=id)
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
                "tip_farma": t_farma,
                "farma_pa":zip(aten_pa,real_far),
                "lista_ate":aten_pa,
                "receta":c_receta,

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
