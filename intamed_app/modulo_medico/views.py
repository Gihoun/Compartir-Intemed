from array import array
from cProfile import run
from cmath import exp
from curses import use_default_colors
from email import message_from_binary_file
from multiprocessing import context
from multiprocessing.sharedctypes import Array
from select import select
from xml.dom import NoDataAllowedErr
from django.shortcuts import render
from django.contrib.auth.models import User
from modulo_admin.models import Agenda, Comuna,Boleta, DetalleFarmaco, Diagnostico, EstadoCivil, Examen, Genero, Medico, Nacionalidad, Paciente, Receta, ResultadoExamen, TipoDiagnostico, TipoExamen, Usuario, Atencion, Farmaco, Prevision, TelefonoUsuario, Telefono
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
### Procedimentos almacenados para insert ####

def insert_DetAtencio(x, y):
    with connection.cursor() as cursor:
        cursor.callproc("sp_detalle_atencion", (x, y))
    return True
def insert_DetFarmaco(x, y):
    with connection.cursor() as cursor:
        cursor.callproc("sp_detalle_farmaco", (x, y))
    return True
def insert_DetAlergia(x, y):
    with connection.cursor() as cursor:
        cursor.callproc("sp_detalle_alergia", (x, y))
    return True

##############################################

@login_required()
def receta_med(request,id):  
    print(id)
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
                    return pdf_receta(request,det_R,id,r.id_receta)
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

@login_required()
def certi_med(request,id):
    ar_id = id.split('-')
    u =  Usuario.objects.get(run = ar_id[1])
    a = Atencion.objects.get(id_atencion = ar_id[0])
    
    if request.POST:
        det_C = request.POST.get("certiP")
        if det_C is not None:
            if det_C.strip() != '':        
                try:                   
                    return pdf_certi(request,det_C,id)
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
    return render(request,"med_certi.html",contexto)

@login_required()
def orden_med(request,id):
    ar_id = id.split('-')
    u =  Usuario.objects.get(run = ar_id[1])
    a = Atencion.objects.get(id_atencion = ar_id[0])
    te =  TipoExamen.objects.all()
    id_ex = Examen.objects.aggregate(maximo=Max('id_examen'))['maximo']
    if request.POST:
        det_o = request.POST.get("ordenP")
        tipo_ex = request.POST.get("inputexa")
        if det_o is not None:
            if det_o.strip() != '':        
                try:                   
                    e = Examen()
                    e.id_examen = id_ex + 2
                    e.nombre_examen = det_o
                    e.id_tipo_exam = TipoExamen.objects.get(tipo_exam=tipo_ex)
                    e.save()

                    return pdf_orden(request,det_o,id,e.id_examen,tipo_ex)
                except:
                    er = 1
                    print('mal')
            else:
                print('mal srp')
                er= 2    
    contexto = {
        "user":u,
        "atencion":a,
        "id":id,
        "tipo_exa":te,
    }
    return render(request,"med_orden.html",contexto)

@login_required()
def pdf_orden(request,det_o,id,id_exa,te):
    ## id ppara personalizar
    logueado = request.user
    run_med = logueado.usuario_django.run_django
    usu_medico = Usuario.objects.get(run=run_med)

    ar_id = id.split('-')
    u =  Usuario.objects.get(run = ar_id[1])
    a = Atencion.objects.get(id_atencion = ar_id[0])
    fecha = a.fecha_atencion
    formato = fecha.strftime("%d-%m-%Y")
    
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    p.drawString(220, 800, f"Orden de Exámen")
    p.drawString(20, 780, f"Nombre Paciente : {u.p_nombre} {u.s_nombre} {u.apellido_pa} {u.apellido_ma}")
    p.drawString(350, 780, f"Folio Orden: O-{id_exa}")
    p.drawString(20, 760, f"Edad                  : {u.edad_actual} años")
    p.drawString(350, 760, f"Sexo: {u.id_genero.nombre_genero}")

    p.drawString(20, 740, f"Direccion           : {u.direccion}")
    p.drawString(20, 720, f"Fecha Emisión  :  {formato} ")
    p.drawString(350,740, f"Direccion clinica: Ovalle #345")
    
    p.line(20,700,570,700)
    p.drawString(20, 680, f"Detalle Orden: ")
    p.drawString(40, 640,f"Tipo exámen: {te}" )
    p.drawString(40, 620, det_o)
    p.line(20, 120, 570, 120)
    
    p.drawString(350, 100, f"Run profesional : {usu_medico.run}-{usu_medico.dv} ")
    p.drawString(350, 80,  f"Medico Tratante : {usu_medico.p_nombre} {usu_medico.apellido_pa} {usu_medico.apellido_ma}")
    p.drawString(350, 60,  f"Especialidad    : Ginecologia")
    p.drawString(20, 100,  f"Servicios de Salud Intemed ")
    p.drawString(20, 80,   f"RUT             : 96.999.888-2 ")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    namefile = 'Pa'+str(id)+'O_'+str(id_exa)+'.pdf'
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=namefile)

@login_required()
def pdf_receta(request,ate,id,id_r):
    logueado = request.user
    run_med = logueado.usuario_django.run_django
    usu_medico = Usuario.objects.get(run=run_med)
    ## id ppara personalizar
    ar_id = id.split('-')
    u =  Usuario.objects.get(run = ar_id[1])
    a = Atencion.objects.get(id_atencion = ar_id[0])
    fecha = a.fecha_atencion
    formato = fecha.strftime("%d-%m-%Y")
    
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
    
    p.drawString(350, 100, f"Run profesional :{usu_medico.run}-{usu_medico.dv} ")
    p.drawString(350, 80, f"Medico Tratante : {usu_medico.p_nombre} {usu_medico.apellido_pa}")
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

@login_required()
def pdf_certi(request,detC,id):
    
    logueado = request.user
    run_med = logueado.usuario_django.run_django
    usu_medico = Usuario.objects.get(run=run_med)
    ## id ppara personalizar
    ar_id = id.split('-')
    u =  Usuario.objects.get(run = ar_id[1])
    a = Atencion.objects.get(id_atencion = ar_id[0])
    fecha = a.fecha_atencion
    formato = fecha.strftime("%d-%m-%Y")
    
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    p.drawString(220, 800, f"Certificado Médico")
    p.drawString(20, 780, f"Nombre Paciente : {u.p_nombre} {u.s_nombre} {u.apellido_pa} {u.apellido_ma}")
    p.drawString(20, 760, f"Edad                  : {u.edad_actual} años")
    p.drawString(350, 760, f"Sexo: {u.id_genero.nombre_genero}")

    p.drawString(20, 740, f"Direccion           : {u.direccion}")
    p.drawString(20, 720, f"Fecha Emisión  :  {formato} ")
    p.drawString(350,740, f"Direccion clinica: [Direccion Clinica X, X] ")
    
    p.line(20,700,570,700)
    p.drawString(20, 680, f"Detalle Certificado: ")
    p.drawString(40, 620, detC)
    p.line(20, 120, 570, 120)
    
    p.drawString(350, 100, f"Run profesional :{usu_medico.run}-{usu_medico.dv} ")
    p.drawString(350, 80, f"Medico Tratante : {usu_medico.p_nombre} {usu_medico.apellido_pa}")
    p.drawString(350, 60, f"Especialidad    : ")
    p.drawString(20, 100, f"Servicios de salud Intemed ")
    p.drawString(20, 80, f"RUT: 96.999.888-2 ")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    namefile = 'Cer'+str(id)+'ti'+formato+'.pdf'
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=namefile)


def genpdf_boleta(request,id):
    arr_1= id.split('-')

    buffer = io.BytesIO()
    bol = Boleta.objects.get(id_atencion=arr_1[0])
    uss = Usuario.objects.get(run=arr_1[1])
    med = Usuario.objects.get(run=arr_1[2])
    img_file = "./modulo_recepcion/static/img/intemed.png"
    valor = bol.monto_pago
    
    p = canvas.Canvas(buffer)
    x_cord = 350
    y_cord = 510
    p.drawImage(img_file, x_cord, y_cord, width=200, preserveAspectRatio=True, mask='auto')
    p.drawString(240, 820, f"BONO DE ATENCION: {arr_1[0]}")
    p.drawString(20, 780, f"Nombre Paciente: {uss.p_nombre} {uss.s_nombre} {uss.apellido_pa} {uss.apellido_ma}")
    p.drawString(20, 760, f"Edad:  {uss.edad_actual} Años")
    p.drawString(20, 740, f"Direccion      : {uss.direccion}")
    p.drawString(20, 720, f"Fecha Emisión  :  {bol.fecha_boleta} ")
    p.drawString(350,720, f"Direccion clinica: Ovalle #347")

    p.drawString(20, 680, f"Detalle Atencion ")

    p.line(20,700,570,700)

    p.drawString(20, 640, f"Atencion: {arr_1[0]}")
    p.drawString(350, 640, f"Por un valor de     : ${valor}")
    
  
    
    p.drawString(350, 570, f"Valor Total a pagar : ${valor}")
    p.line(20, 600, 570, 600)

    
    p.drawString(20, 500, f"Run profesional : {med.run}-{med.dv}")
    p.drawString(20, 480, f"Medico Tratante : {med.p_nombre} {med.apellido_pa} {med.apellido_ma}")
    p.drawString(20, 460, f"Especialidad    : Ginecologia ")

    p.drawString(350, 500, f"Servicios de salud Intamed ")
    p.drawString(350, 480, f"RUT: 96.999.888-2 ")

    p.drawString(350, 460, f"Firma Institucion")

    p.showPage()
    p.save()

    buffer.seek(0)

    filname = 'boleta' + str(id) + '.pdf'
    
    return FileResponse(buffer, as_attachment=True, filename=filname)


@login_required()
def inicio(request):

    logueado = request.user
    run_med = logueado.usuario_django.run_django
    usu_medico = Usuario.objects.get(run=run_med)
    contexto = {"medico": usu_medico}
    return render(request, "index_medico.html", contexto)

@login_required()
def agenda(request):
    # obtiene el medico autenticado
    logueado = request.user
    run_med = logueado.usuario_django.run_django
    usu_medico = Usuario.objects.get(run=run_med)


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
    u_p = Usuario.objects.filter(run__in=det_age)

    r_p = list(det_agenda.objects.values_list('run_pac').filter(idd__in=disp))
    array_p=[]
    for p in r_p:
        array_p.append(p[0])
    
    user_p = Usuario.objects.filter(run__in=array_p)


    


    ################################
    contexto = {
        "pacientes": pacientes,
        "antiguo": zip(user_p, array_antiguedad,det_age),
        "disponibilidad": disp,
        "medico": usu_medico,
        "agenda": det_age
    }
    return render(request, "agenda_paciente.html", contexto)

@login_required()
def atePaciente(request, id):
    logueado = request.user
    run_med = logueado.usuario_django.run_django
    usu_medico = Usuario.objects.get(run=run_med)

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
    id_diag = Diagnostico.objects.aggregate(maximo=Max('id_diagnostico'))['maximo']
    list_ate=[]
    last_detAt = DetalleAtencion.objects.filter(run_paciente=id)
    ids_ate = list(last_detAt.values_list("id_atencion"))
    for id in ids_ate:
        list_ate.append(id[0]) 
    try:
        aten_pa = Atencion.objects.get(id_atencion__in=list_ate)
    except:
        aten_pa= None


    c_receta= str(aten_pa.id_atencion)+'-'+str(usuario.run)
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
        idr_actual = Receta.objects.aggregate(maximo=Max('id_receta'))['maximo']
        receta = Receta.objects.get(id_receta=idr_actual)
        
        ################## Orden Examen = O ##################################    
        ido_actual = Examen.objects.aggregate(maximo=Max('id_examen'))['maximo']
        orden = Examen.objects.get(id_examen=ido_actual)


        ################## Receta Paciente = A ##################################
        a_get = request.POST.get('inputDetalleA')
        # Alergias cortadas para su identificacion
        split_ale = a_get.split()

        if x.talla is not None and x.peso is not None and x.imc is not None and x.observaciones is not None and x.cirugias is not None and x.enfermedades is not None and x.medicacion_habitual:
            if x.talla.strip() != '' and x.peso.strip() != '' and x.imc.strip() != '' and x.observaciones.strip() != '' and x.cirugias.strip() != '' and x.enfermedades.strip() != '' and x.medicacion_habitual:
                try:
                    z.save()

                    ################### Detalle Farmaco = dt ####################################
                    for f in farmaname:
                        fa = Farmaco.objects.get(nombre_farmaco=f)
                        #insert_DetFarmaco(r.id_receta, fa.id_farmaco)
                    #### Valores Registro Atencion = Y ############################# 
                    aten_pa.id_diagnostico = Diagnostico.objects.get(id_diagnostico=z.id_diagnostico)
                    aten_pa.exploracion_clinica = request.POST.get("inputExplo")
                    if receta.id_receta is not None:
                        aten_pa.id_receta = Receta.objects.get(id_receta=receta.id_receta)
                    else:
                        aten_pa.id_receta = None
                    if orden.id_examen is not None:
                        aten_pa.id_examen = Examen.objects.get(id_examen=orden.id_examen)
                    else:
                        aten_pa.id_examen = None
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
        "atencion": aten_pa,
        "medico": usu_medico,
        "receta":c_receta,

    }
    return render(request, "atencion_paciente.html", contexto)




@login_required()
def consultaV(request):
    logueado = request.user
    run_med = logueado.usuario_django.run_django
    usu_medico = Usuario.objects.get(run=run_med)
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
        print(run_paciente)
        user_c = Usuario.objects.all().filter(run=run_paciente).count()
        pa_u =  Usuario.objects.get(run=run_paciente)
        print(user_c)

        if user_c > 0:
            response = redirect('modulo_medico:consultaP',id=run_paciente)
            return response #consultaP(request,run_paciente)
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
                        "medico": usu_medico,
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
                    "existe": mensaje,
                    "tip_diag": t_diag,
                    "medico": usu_medico,
                    }
        return render(request, "consulta_paciente.html", contexto)

@login_required()
def consultaP(request, id):
    logueado = request.user
    run_med = logueado.usuario_django.run_django
    usu_medico = Usuario.objects.get(run=run_med)
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


    ################## Receta Paciente = R ##################################
    idr_actual = Receta.objects.aggregate(maximo=Max('id_receta'))['maximo']
    receta = Receta.objects.get(id_receta=idr_actual)
        
    ################## Orden Examen = O ##################################    
    ido_actual = Examen.objects.aggregate(maximo=Max('id_examen'))['maximo']
    orden = Examen.objects.get(id_examen=ido_actual)

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

        ################## Receta Paciente = A ##################################
        a_get = request.POST.get('inputDetalleA')
        # Alergias cortadas para su identificacion
        split_ale = a_get.split()

        if user.correo is not None and user.direccion is not None and user.id_comuna is not None and user.id_estado is not None and x.talla is not None and x.peso is not None and x.observaciones is not None and x.cirugias is not None and x.enfermedades is not None and x.medicacion_habitual:
            if user.correo.strip() != '' and user.direccion.strip() != '' and x.talla.strip() != '' and x.peso.strip() != '' and x.observaciones.strip() != '' and x.cirugias.strip() != '' and x.enfermedades.strip() != '' and x.medicacion_habitual:
                try:
                    z.save()              
                    ################### Detalle Farmaco = dt ####################################
                    for f in farmaname:
                        fa = Farmaco.objects.get(nombre_farmaco=f)
                        #insert_DetFarmaco(r.id_receta, fa.id_farmaco)
                    #### Valores Registro Atencion = Y #############################
                    id_ate.id_diagnostico = Diagnostico.objects.get(id_diagnostico=z.id_diagnostico)
                    id_ate.exploracion_clinica = request.POST.get("inputExplo")
                    if receta.id_receta is not None:
                        id_ate.id_receta = Receta.objects.get(id_receta=receta.id_receta)
                    else:
                        id_ate.id_receta = None
                    if orden.id_examen is not None:
                        id_ate.id_examen = Examen.objects.get(id_examen=orden.id_examen)
                    else:
                        id_ate.id_examen = None
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
                    #return redirect('modulo_medico:consultaP', h=id)
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
                "medico": usu_medico,

                }
    return render(request, "consulta_paciente.html", contexto)

@login_required()
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
