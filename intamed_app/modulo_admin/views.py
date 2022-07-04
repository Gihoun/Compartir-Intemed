from cProfile import run
from multiprocessing import context
from multiprocessing.sharedctypes import Array
from select import select
from .metodos import *
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *
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

def administrator(request):
    #Dash por Defecto
    logger = logging.getLogger(__name__)
    users_all = Usuario.objects.all().count()
    annios = list(Atencion.objects.values_list("fecha_atencion__year"))
    
    arr_annios=[]
    
    for a in annios:
        if a[0] not in arr_annios:
            arr_annios.append(a[0])
    arr_annios.sort()
    if request.POST:
        annio = request.POST.get("annio")
        logger.warning(annio)
        ate_year = Atencion.objects.filter(fecha_atencion__year=annio)

        ate_mes1 = ate_year.filter(fecha_atencion__month=1).count()
        ate_mes2 = ate_year.filter(fecha_atencion__month=2).count()
        ate_mes3 = ate_year.filter(fecha_atencion__month=3).count()
        ate_mes4 = ate_year.filter(fecha_atencion__month=4).count()
        ate_mes5 = ate_year.filter(fecha_atencion__month=5).count()
        ate_mes6 = ate_year.filter(fecha_atencion__month=6).count()
        ate_mes7 = ate_year.filter(fecha_atencion__month=7).count()
        ate_mes8 = ate_year.filter(fecha_atencion__month=8).count()
        ate_mes9 = ate_year.filter(fecha_atencion__month=9).count()
        ate_mes10 = ate_year.filter(fecha_atencion__month=10).count()
        ate_mes11 = ate_year.filter(fecha_atencion__month=11).count()
        ate_mes12 = ate_year.filter(fecha_atencion__month=12).count()
        contexto1 = {"cant":users_all,
                "annios":arr_annios,
                "ene":ate_mes1,
                "feb":ate_mes2,
                "mar":ate_mes3,
                "abr":ate_mes4,
                "may":ate_mes5,
                "jun":ate_mes6,
                "jul":ate_mes7,
                "ago":ate_mes8,
                "sep":ate_mes9,
                "oct":ate_mes10,
                "nov":ate_mes11,
                "dic":ate_mes12
                }
        return JsonResponse(contexto1, status=200)
        
    else:
        ate_year = Atencion.objects.filter(fecha_atencion__year=2010)
        ate_mes1 = ate_year.filter(fecha_atencion__month=1).count()
        ate_mes2 = ate_year.filter(fecha_atencion__month=2).count()
        ate_mes3 = ate_year.filter(fecha_atencion__month=3).count()
        ate_mes4 = ate_year.filter(fecha_atencion__month=4).count()
        ate_mes5 = ate_year.filter(fecha_atencion__month=5).count()
        ate_mes6 = ate_year.filter(fecha_atencion__month=6).count()
        ate_mes7 = ate_year.filter(fecha_atencion__month=7).count()
        ate_mes8 = ate_year.filter(fecha_atencion__month=8).count()
        ate_mes9 = ate_year.filter(fecha_atencion__month=9).count()
        ate_mes10 = ate_year.filter(fecha_atencion__month=10).count()
        ate_mes11 = ate_year.filter(fecha_atencion__month=11).count()
        ate_mes12 = ate_year.filter(fecha_atencion__month=12).count()
        contexto = {"cant":users_all,
                    "annios":arr_annios,
                    "ene":ate_mes1,
                    "feb":ate_mes2,
                    "mar":ate_mes3,
                    "abr":ate_mes4,
                    "may":ate_mes5,
                    "jun":ate_mes6,
                    "jul":ate_mes7,
                    "ago":ate_mes8,
                    "sep":ate_mes9,
                    "oct":ate_mes10,
                    "nov":ate_mes11,
                    "dic":ate_mes12
                    }
    return render(request,"administrator.html",contexto)

def filtro_usuarios(request):
    arr_id=[1,2,3]
    users_all = Usuario.objects.filter(id_perfil__in = arr_id)
    users_cant = users_all.count()
    if request.POST:
        busqueda = request.POST.get("txbusqueda")
        eliminar = request.POST.get("eliminar")
        if eliminar is not None:
            usu = Usuario.objects.get(run=eliminar)
            usu.delete()
            print("Colaborador Eliminado Exitosamente")
            messages.success(request, "Colaborador Eliminado Exitosamente")
            users_ret = Usuario.objects.filter(id_perfil__in = arr_id)
            users_cant = users_ret.count()
        elif busqueda is not None:
            users_ret = Usuario.objects.filter(run__startswith=busqueda, id_perfil__in = arr_id)
            users_cant = users_ret.count()
        else:
            users_ret = Usuario.objects.all()
            users_cant = users_ret.count()
        contexto = {"usuarios":users_ret,"cantidad":users_cant}
    else:
        users_all = Usuario.objects.all().filter(id_perfil__in = arr_id)
        contexto = {"usuarios":users_all,"cantidad":users_cant}
    return render(request, 'usuarios_s.html', contexto)

def filtro_pacientes(request):
    if request.POST:
        busqueda = request.POST.get("txbusqueda")
        eliminar = request.POST.get("eliminar")
        if eliminar is not None:
            paciente = Usuario.objects.get(run=eliminar)
            paciente.delete()
            print("Paciente Eliminado Exitosamente")
            messages.success(request, "Paciente Eliminado Exitosamente")
            users_ret = Usuario.objects.filter(id_perfil=4)[:25]
            users_cant = users_ret.count()
        elif busqueda is not None:
            users_ret = Usuario.objects.filter(run__startswith=busqueda,id_perfil=4)
            users_cant = users_ret.count()
        else:
            users_ret = Usuario.objects.all()
            users_cant = users_ret.count()
        contexto = {"usuarios":users_ret,"cantidad":users_cant}

        if users_cant>=1:
            contexto = {"usuarios":users_ret,"cantidad":users_cant}
        else:
            contexto = {"usuarios":0,"cantidad":0}
    else:
        users_pac = Usuario.objects.all().filter(id_perfil=4).select_related('paciente')[:25]
        userp_cant = users_pac.count()
        contexto = {"usuarios":users_pac,"cantidad":userp_cant}
    return render(request, 'pacientes_s.html', contexto)

def edit_paciente(request,id):
    logger = logging.getLogger(__name__)
    mensaje = ''

    prevision = Prevision.objects.all()
    tel_users = TelefonoUsuario.objects.filter(run_usuario=id).values_list('id_telefono', flat=True) 
    num_tel = Telefono.objects.all().filter(id_telefono__in=tel_users).values_list('num_telefono', flat=True)
    cant_tel = tel_users.count() 
    cant = num_tel.count()
    paciente = Usuario.objects.get(run=id)
    paciente_real = Paciente.objects.get(run_paciente=id)
    comunas = Comuna.objects.all()
    nacionalidades = Nacionalidad.objects.all()
    estados = EstadoCivil.objects.all()
    generos = Genero.objects.all()

    todo_alergias = Alergia.objects.all()
    aler_user = DetalleAlergia.objects.filter(run_paciente=id).values_list('id_alergia',flat=True)
    alergias = Alergia.objects.all().filter(id_alergia__in=aler_user).values_list('nombre_alergia', flat=True)

    if request.POST:
        ## CAMPOS INCLUSIVOS DE USUARIO
        p_nom = request.POST.get("inputPNom")
        s_nom = request.POST.get("inputSNom")
        nom_soc = request.POST.get("inputNomSoc")
        ap_pa = request.POST.get("inputAp")
        ap_ma = request.POST.get("inputAM")
        com_p = request.POST.get("inputComPac")
        dir_p = request.POST.get("inputDir")
        correo_p = request.POST.get("inputCorreo")
        nac_p = request.POST.get("inputNacPac")
        fec_nacP = request.POST.get("fecha")
        est_p = request.POST.get("inputEstadoPac")
        gen_p = request.POST.get("inputGeneroPac")
        tel_p = request.POST.get("inputFono")## OJO CON EL TELEFONO
        
        ## CAMPOS EXCLUSIVOS DE PACIENTE
        talla = request.POST.get("inputTalla")
        peso = request.POST.get("inputPeso")
        prev = request.POST.get("inputPrev")
        
        
        flag , userr = editar_usuario_gral(id, p_nom, s_nom, nom_soc, ap_pa, ap_ma, com_p, dir_p, correo_p, nac_p, fec_nacP, est_p, gen_p)
        if flag:
            try:##FALTA ALERGIAS Y TELEFONOS
                prevP = Prevision.objects.get(nombre_prevision=prev)
                paciente_real.id_prevision = prevP
                paciente_real.talla = talla
                paciente_real.peso = peso
                paciente_real.save()
                messages.success(request, "Paciente Editado Exitosamente")
                mensaje="paciente guardado exitosamente"
                contexto = {"paciente": userr, "prevision": prevision, "telefonos": num_tel, "cantidad": cant_tel,
                "comuna": comunas, "nacionalidad": nacionalidades, "estado": estados, "genero": generos, "alergias": alergias,"alers":todo_alergias}
            except:
                mensaje="usuario base guardado problemas en paciente"
        else:
            mensaje="problemas al guardar usuario base"
    logger.warning(mensaje)
    contexto = {"paciente": paciente, "prevision": prevision, "telefonos": num_tel, "cantidad": cant_tel,
                "comuna": comunas, "nacionalidad": nacionalidades, "estado": estados, "genero": generos, "alergias": alergias,"alers":todo_alergias}
    return render(request, 'edit_paciente.html',contexto)

def vista_farmaco(request):
    farmacos = Farmaco.objects.all()
    farmaco_cant = farmacos.count()
    if request.POST:
        busqueda = request.POST.get("txbusqueda")
        eliminar = request.POST.get("eliminar")

        if eliminar is not None:
            far = Farmaco.objects.get(id_farmaco=eliminar)
            far.delete()
            print("Fármaco Eliminado Exitosamente")
            messages.success(request, "Fármaco Eliminado Exitosamente")
            farmacos = Farmaco.objects.all()
            farmaco_cant = farmacos.count()
            contexto = {"farmacos":farmacos,"cantidad":farmaco_cant}
        elif busqueda is not None:
            farmacos = Farmaco.objects.filter(nombre_farmaco__startswith=busqueda)
            farmaco_cant = farmacos.count()
        else:
            farmacos = Farmaco.objects.all()
            farmaco_cant = farmacos.count()
        contexto = {"farmacos":farmacos,"cantidad":farmaco_cant}
        if farmaco_cant>=1:
            contexto = {"farmacos":farmacos,"cantidad":farmaco_cant}
        else:
            contexto = {"farmacos":0,"cantidad":0}
    else:
        contexto = {"farmacos":farmacos,"cantidad":farmaco_cant}
    return render(request, 'farmacos.html', contexto)


def edit_farmaco(request,id):
    logger = logging.getLogger(__name__)
    tipo_farmacos= TipoFarmaco.objects.all()
    farmaco_todos =  Farmaco.objects.get(id_farmaco=id)
    mensaje=''
    if request.POST:
        n_farm = request.POST.get("nombre_farma")
        v_adm = request.POST.get("via_adm")
        contraind = request.POST.get("contra_ind")
        tipo_farm = request.POST.get("tipo_farma")
        try:
            farma= Farmaco.objects.get(id_farmaco=id)
            t_farm= TipoFarmaco.objects.get(tipo_farma=tipo_farm)
            
            farma.id_tipo_farma = t_farm
            if n_farm is not None and contraind is not None and v_adm is not None :
                if n_farm.strip() !='' and contraind.strip() !='' and v_adm.strip() !='' :
                    farma.nombre_farmaco = n_farm
                    farma.via_administracion = v_adm
                    farma.contraindicacion = contraind.strip()
                    farma.save()
                    flag=True
                    mensaje="Fármaco Modificado con Éxito"
            else:
                mensaje="Fármaco con Campos No Válidos"
                flag=False 
            
            contexto = {"farmaco": farma,"tipos": tipo_farmacos,"mensaje": mensaje}
            messages.info(request, mensaje)
            logger.warning(mensaje)
        except:
            flag=False
            mensaje="El Fármaco no ha Podido ser Modificado"
            messages.info(request, mensaje)
            logger.warning(mensaje)
            contexto = {"farmaco": farmaco_todos,"tipos": tipo_farmacos,"mensaje": farma}
    else:
        contexto = {"farmaco": farmaco_todos,"tipos": tipo_farmacos,"mensaje": mensaje}
    return render(request, 'edit_farma.html', contexto)

def vista_perfil(request):
    perfiles = PerfilUsuario.objects.all()
    perfiles_cant = perfiles.count()
    if request.POST:
        busqueda = request.POST.get("txbusqueda")
        eliminar = request.POST.get("eliminar")

        if eliminar is not None:
            per = PerfilUsuario.objects.get(id_perfil=eliminar)
            per.delete()
            print("Perfil Eliminado Exitosamente")
            messages.success(request, "Perfil de Usuario Eliminado Exitosamente")
            perfiles = PerfilUsuario.objects.all()
            perfiles_cant = perfiles.count()
            contexto = {"perfiles":perfiles,"cantidad":perfiles_cant}
        elif busqueda is not None:
            perfiles = PerfilUsuario.objects.filter(nombre_perfil__startswith=busqueda)
            perfiles_cant = perfiles.count()
        else:
            perfiles = PerfilUsuario.objects.all()
            perfiles_cant = perfiles.count()
        contexto = {"perfiles":perfiles,"cantidad":perfiles_cant}
        if perfiles_cant>=1:
            contexto = {"perfiles":perfiles,"cantidad":perfiles_cant}
        else:
            contexto = {"perfiles":0,"cantidad":0}
    else:
        contexto = {"perfiles":perfiles,"cantidad":perfiles_cant}
    return render(request, 'perfiles.html', contexto)

def edit_perfil(request,id):
    logger = logging.getLogger(__name__)
    perfiles = PerfilUsuario.objects.get(id_perfil=id)
    mensaje=''
    if request.POST:
        n_perfil = request.POST.get("nom_prefil")
        try:
            perfil = PerfilUsuario.objects.get(id_perfil=id)
            if n_perfil is not None:
                if n_perfil.strip() !='':
                    perfil.nombre_perfil = n_perfil
                    perfil.save()
                    
                    mensaje="Perfil de Usuario Modificado con Éxito"
            else:
                mensaje="Edición de Perfil Inválida"
                 
            contexto = {"perfil": perfil,"mensaje": mensaje}
            messages.info(request, mensaje)
            logger.warning(mensaje)
        except:
            
            mensaje="Perfil de Usuario No Modificado"
            messages.info(request, mensaje)
            logger.warning(mensaje)
            contexto = {"perfil": perfiles,"mensaje": perfil}
    else:
        contexto = {"perfil": perfiles,"mensaje": mensaje}
    return render(request, 'edit_perfil.html', contexto)

def edit_colab(request,id):
    logger = logging.getLogger(__name__)
    colab = Usuario.objects.get(run=id)
    id_perfil = colab.id_perfil_id
    tel_users = TelefonoUsuario.objects.filter(run_usuario=id).values_list('id_telefono', flat=True)
    cant_tel = tel_users.count()    
    num_tel = Telefono.objects.all().filter(id_telefono__in=tel_users).values_list('num_telefono', flat=True)
    comunas= Comuna.objects.all()
    nacionalidades = Nacionalidad.objects.all()
    estados = EstadoCivil.objects.all()
    generos = Genero.objects.all()

    mensaje=''
    arr_tel=[]

    if request.POST:
        # Campos a Modificar propios de la Tabla Usuario:
        p_nom = request.POST.get("inputPNom")
        s_nom = request.POST.get("inputSNom")
        nom_soc = request.POST.get("inputNomSoc")
        ap_pa = request.POST.get("inputAp")
        ap_ma = request.POST.get("inputAM")
        com_colab = request.POST.get("inputComuna")
        dir_colab = request.POST.get("inputDir")
        correo_colab = request.POST.get("inputCorreo")
        nac_colab = request.POST.get("inputNac")
        fec_nac_colab = request.POST.get("inputFechaNac")
        est_colab = request.POST.get("inputEstado")
        gen_colab = request.POST.get("inputGenero")
        tel_colab = request.POST.get("inputFono")
        # Campos a Modificar propios de la Tabla Administrador, Médico y Recepcionista:
        arr_tel.append(tel_colab)

        if id_perfil == 1:
            fec_ing_colab = request.POST.get("inputFechaIngreso")
            sueldo = request.POST.get("inputSueldo")
        elif id_perfil == 2:
            fec_ing_colab = request.POST.get("inputFechaIngreso")
            sueldo = request.POST.get("inputSueldo")
            print(f'este es su sueldo {sueldo}')
            reg_hrs = request.POST.get("inputRegimenHrs")
        elif id_perfil == 3:
            fec_ing_colab = request.POST.get("inputFechaIngreso")
            sueldo = request.POST.get("inputSueldo")        
        # Proceso de Modificación de los Campos
        flag ,usr = editar_usuario_gral(id, p_nom, s_nom, nom_soc, ap_pa, ap_ma, com_colab, dir_colab, correo_colab, nac_colab, fec_nac_colab, est_colab, gen_colab)
        if flag:
            
            flag2 , mensaje = save_tel_varios(id,arr_tel)
            print(f" la bandera segunda {flag2}")
            if flag2 == 3:
                for t in arr_tel:
                    if t.strip() != '' and t is not None:
                        mensaje = save_tel_unico(id,t)
                        logger.warning(mensaje)
            try:

                
                if id_perfil == 1:
                    admin = Administrador.objects.get(run_admin=id)
                    admin.fecha_ingreso = fec_ing_colab
                    admin.sueldo = sueldo
                    admin.save()
                    logger.warning("admin guardado")
                    mensaje="Administrador Modificado con Éxito"
                    
                elif id_perfil == 2:
                    print(f'usuario medicxo{id}')
                    medico = Medico.objects.get(run_medico=id)
                    print(f'usuario medicxo {medico}')
                    medico.fecha_ingreso = fec_ing_colab
                    print(f'fi medicxo {medico}')
                    medico.sueldo = sueldo
                    print(f'sukdo medicxo {medico}')
                    medico.regimen_hrs = reg_hrs
                    print(f'reghoras medicxo {medico}')
                    medico.save()
                    mensaje="Medico Modificado con Éxito"
                    
                elif id_perfil == 3:
                    recep = Recepcionista.objects.get(run_recepcionista=id)
                    recep.fec_ing_colab = fec_ing_colab
                    recep.sueldo = sueldo
                    recep.save()
                    mensaje="Recepcionista Modificado con Éxito"
                    
                
                contexto = {"colab": usr, "telefonos": num_tel, "cantidad": cant_tel, "comuna": comunas, 
                            "nacionalidad":nacionalidades, "estado":estados, "genero":generos,"mensaje": mensaje}
            except:
                mensaje="usuario base guardado pero hay error en campos especificos del perfil"
                logger.warning(mensaje)
                contexto = {"colab": usr, "telefonos": num_tel, "cantidad": cant_tel, "comuna": comunas, 
                            "nacionalidad":nacionalidades, "estado":estados, "genero":generos,"mensaje": mensaje}
        else:
            mensaje="Error en los campos basicos del usuario "
             
    # SIN POST
    else:
        contexto = {"colab": colab, "telefonos": num_tel, "cantidad": cant_tel, "comuna": comunas, 
                    "nacionalidad":nacionalidades, "estado":estados, "genero":generos, "mensaje": mensaje}
    return render(request, 'edit_usuario.html', contexto)

def vista_atenciones(request,id):
    usrs = Usuario.objects.all()
    atenciones = Atencion.objects.all()
    cant_tot= Atencion.objects.filter(fecha_atencion__year=id).count()

    ate_year = Atencion.objects.filter(fecha_atencion__year=id)[:16]
    atenciones_cant = ate_year.count()
    
    annios = list(Atencion.objects.values_list("fecha_atencion__year"))
    
    arr_annios=[]
    arr_ids=[]
    
    for a in annios:
        if a[0] not in arr_annios:
            arr_annios.append(a[0])
    
    ids = ate_year.values_list("id_atencion")
    for e in ids:
        arr_ids.append(e[0])
    if request.POST:
        arr_2=[]
        arr_f=[]
        run_b = request.POST.get("btn_run")
        run_i= request.POST.get("input_run")
        if run_i is not None: 
            if run_i.strip()!= '':
                ru = run_i
            else:
                ru = 0
        else:
            ru = run_b
        det_at_selected = DetalleAtencion.objects.filter(run_paciente=ru)
        cant_pac= det_at_selected.count()
        id_at= list(det_at_selected.values_list("id_atencion"))
        for f in id_at:
            arr_2.append(f[0])
        ate_pac= Atencion.objects.filter(id_atencion__in=arr_2).order_by('fecha_atencion__year')
        for t in ate_pac:
            annio = t.fecha_atencion.year
            if annio not in arr_f:
                arr_f.append(annio) 
        if len(arr_f) != 0:
            an = f" {min(arr_f)} -- {max(arr_f)} "
            sel= det_at_selected.values_list("run_paciente","id_atencion")
        else:
            an = id
            ate_pac=0
            cant_pac=0
            det_at_selected=''
            sel=0
            r=0
        r="Reservado"
        contexto = {"atencion":ate_pac,"cantidad":cant_pac,"detalle":det_at_selected, "annios":arr_annios, "fecha":an,"selc": sel, "diag": r}
    else:
        det_at_selected = DetalleAtencion.objects.filter(id_atencion__in=arr_ids).select_related('run_paciente')
        sel= det_at_selected.values_list("run_paciente","id_atencion")
        contexto = {"atencion":ate_year,"cantidad":atenciones_cant,"c_total":cant_tot, "detalle":det_at_selected,"annios":arr_annios,"fecha":id,"selc": sel}
    return render(request, 'atenciones.html', contexto)

def vista_reportes(request):
    reportes = Reporte.objects.all()
    report_cant = reportes.count()
    if request.POST:
        busqueda = request.POST.get("txbusqueda")
        report_selected = Reporte.objects.filter(id_reporte__startswith=busqueda)
        report_cant = report_selected.count()
        contexto = {"reportes":report_selected,"cantidad":report_cant}
    else:
        contexto = {"reportes":reportes,"cantidad":report_cant}
    return render(request, 'reportes.html', contexto)

def vista_newcolab(request):
    arr_id=[1,2,3]
    comunas = Comuna.objects.all()
    estado = EstadoCivil.objects.all()
    generos = Genero.objects.all()
    nacionalidades = Nacionalidad.objects.all()
    perfil = PerfilUsuario.objects.filter(id_perfil__in= arr_id)

    if request.POST:
        x = Usuario()
        y = Administrador()
        w = Medico()
        z = Recepcionista()
        x.run = request.POST.get('inputRut')
        x.dv = request.POST.get('inputDV')
        x.p_nombre = request.POST.get('inputPNom')
        x.nombre_social = request.POST.get('inputNomSoc')
        x.s_nombre = request.POST.get('inputSNom')
        x.apellido_pa = request.POST.get('inputAp')
        x.apellido_ma = request.POST.get('inputAM')
        x.direccion = request.POST.get('inputDir')
        x.correo = request.POST.get('inputCorreo')
        x.fecha_nac = request.POST.get('fechaNac')  
        x.contrasena = "temporal123"
        
        # LLAMADA AL OBJETO PERFIL
        id_p = request.POST.get('inputPerfil')
        pperfil = PerfilUsuario.objects.get(id_perfil=id_p)
        x.id_perfil = pperfil
        
        # LLAMADA AL OBJETO NACIONALIDAD
        id_nnac = request.POST.get('inputNac') 
        nnacionalidad = Nacionalidad.objects.get(id_nacionalidad=id_nnac)
        x.id_nacionalidad = nnacionalidad

        # LLAMADA AL OBJETO ESTADO CIVIL
        id_estC = request.POST.get('inputEstadoCivil')
        eestado = EstadoCivil.objects.get(id_estado=id_estC) 
        x.id_estado = eestado

        # LLAMADA AL OBJETO GENERO
        id_ggen = request.POST.get('inputGenero')
        ggenero = Genero.objects.get(id_genero=id_ggen)
        x.id_genero = ggenero

        # LLAMADA AL OBJETO COMUNA
        id_ccom = request.POST.get('inputComuna')
        ccomuna = Comuna.objects.get(id_comuna=id_ccom)
        x.id_comuna = ccomuna

        # LLAMADA AL OBJETO CONTRATO por defecto
        contra = Contrato.objects.get(id_contrato=990)

        if x.id_perfil_id == 1: ## admin

            y.fecha_ingreso = request.POST.get('fechaIng')
            y.sueldo = request.POST.get('inputSueldo')
            y.id_contrato = contra

        elif x.id_perfil_id == 2: ## MEDICO
            ag = Agenda.objects.get(id_agenda=999) ## por defecto
            esp = Especialidad.objects.get(id_espec=1) ## por defecto
            w.fecha_ingreso = request.POST.get('fechaIng')
            w.sueldo = request.POST.get('inputSueldo')
            w.regimen_hrs = request.POST.get('inputRegimenHrs')
            w.id_contrato = contra
            w.id_agenda = ag
            w.id_espec = esp

        elif x.id_perfil_id == 3: ## recepcion
            
            z.fecha_ingreso = request.POST.get('fechaIng')
            z.sueldo = request.POST.get('inputSueldo')
            z.id_contrato = contra

        if x.run is not None and x.dv is not None and x.p_nombre is not None and x.apellido_pa is not None and x.apellido_ma is not None and x.direccion is not None and x.correo is not None and x.contrasena is not None:
            if x.run.strip() !='' and x.dv.strip() !='' and x.p_nombre.strip() !='' and x.apellido_pa.strip() !='' and x.apellido_ma.strip() !='' and x.direccion.strip() !='' and x.correo.strip() !='' and x.contrasena.strip() !='':
                try:
                    x.save()
                    print("Colaborador Registrado")
                    # SE CREA EL OBJETO USUARIO LISTO PARA SER VINCULADO
                    user_obj = Usuario.objects.get(run=x.run)

                    if x.id_perfil_id == 1:
                        y.run_admin = user_obj
                        y.save()
                        print("Administrador Registrado")
                    elif x.id_perfil_id == 2:
                        w.run_medico = user_obj
                        w.save()
                        print("Médico Registrado")
                    elif x.id_perfil_id == 3:
                        z.run_recepcionista = user_obj
                        z.save()
                        print("Recepcionista Registrado")
                    else:
                        print("Colaborador Mal Registrado")

                    contexto = {"estadoCivil":estado, "perfiles": perfil, "comuna":comunas, "genero": generos, "nacionalidad": nacionalidades}
                    return render(request,"crear_colab.html",contexto)
                except:
                    print("Excepción 1")
                    contexto = {"estadoCivil":estado, "perfiles": perfil, "comuna":comunas, "genero": generos, "nacionalidad": nacionalidades}
                    return render(request,"crear_colab.html",contexto)
    else:
        print("Excepción 2")
        contexto = {"estadoCivil":estado, "perfiles": perfil, "comuna":comunas, "genero": generos, "nacionalidad": nacionalidades}
        return render(request,"crear_colab.html",contexto)

def vista_newdrug(request):
    tipos = TipoFarmaco.objects.all()
    if request.POST:
        x = Farmaco()
        x.nombre_farmaco = request.POST.get('inputNF')
        x.via_administracion = request.POST.get('inputVia')
        x.contraindicacion = request.POST.get('inputContra')

        id_tf = request.POST.get('inputTF')
        tipo_farmaco = TipoFarmaco.objects.get(id_tipo_farma=id_tf) 
        x.id_tipo_farma = tipo_farmaco

        num_id = Farmaco.objects.all().prefetch_related().order_by("id_farmaco")
        x.id_farmaco = id(num_id)

        if x.nombre_farmaco is not None and x.via_administracion is not None and x.contraindicacion is not None:
            if x.nombre_farmaco.strip() !='' and x.via_administracion.strip() !='' and x.contraindicacion.strip() !='':
                x.save()
                print("Fármaco Registrado")
            else:
                print("Cayó en el Else")
            contexto = {"tipos": tipos}
            return render(request, "crear_farma.html", contexto)
        contexto = {"tipos": tipos}
        return render(request, "crear_farma.html", contexto)
    else:
        contexto = {"tipos": tipos}
        return render(request, "crear_farma.html", contexto)

def vista_newperfil(request):
    if request.POST:
        p = PerfilUsuario()
        p.nombre_perfil = request.POST.get('inputNombrePerfil')

        num_id = PerfilUsuario.objects.all().prefetch_related().order_by("id_perfil")
        p.id_perfil = id(num_id)

        if p.nombre_perfil is not None:
            if p.nombre_perfil.strip() !='':
                p.save()
                print("Perfil Registrado")
            else:
                print("Perfil dentro del Else")
            return render(request, "crear_perfil.html")
        return render(request, "crear_perfil.html")
    else:
        return render(request, "crear_perfil.html")

def vista_newpac(request):
    comunas = Comuna.objects.all()
    nacionalidades = Nacionalidad.objects.all()
    estados = EstadoCivil.objects.all()
    generos = Genero.objects.all()
    previsiones = Prevision.objects.all()

    if request.POST:
        x = Usuario()
        y = Paciente()

        new_run_pac = request.POST.get('inputRutPaciente')
        #x.run = request.POST.get('inputRutPaciente')
        x.dv = request.POST.get('inputDVPaciente')
        x.p_nombre = request.POST.get('inputPrimerNombrePac')
        x.nombre_social = request.POST.get('inputNombreSocialPac')
        x.s_nombre = request.POST.get('inputSegundoNombrePac')
        x.apellido_pa = request.POST.get('inputApellidoPaPac')
        x.apellido_ma = request.POST.get('inputApellidoMaPac')
        x.direccion = request.POST.get('inputDirPac')
        x.correo = request.POST.get('inputCorreoP')
        x.fecha_nac = request.POST.get('FechaNacPac')  
        x.contrasena = "temporal123"

        id_estC = request.POST.get('inputEstadoPac')
        eestado = EstadoCivil.objects.get(id_estado=id_estC) 
        x.id_estado = eestado

        id_ggen = request.POST.get('inputGeneroPac')
        ggenero = Genero.objects.get(id_genero=id_ggen)
        x.id_genero = ggenero

        id_nnac = request.POST.get('inputNacPac') 
        nnacionalidad = Nacionalidad.objects.get(id_nacionalidad=id_nnac)
        x.id_nacionalidad = nnacionalidad

        id_ccom = request.POST.get('inputComPac')
        ccomuna = Comuna.objects.get(id_comuna=id_ccom)
        x.id_comuna = ccomuna

        perfilu = PerfilUsuario.objects.get(id_perfil=4)
        x.id_perfil = perfilu

        y.peso = request.POST.get('inputPeso')
        y.talla = request.POST.get('inputTalla')

        id_previ = request.POST.get('inputPrev')
        pprev = Prevision.objects.get(id_prevision=id_previ)
        y.id_prevision = pprev

        try:
            user = Usuario.objects.get(run=new_run_pac)
            print("RUT ya Existe")
            print(user.run)
        except:
            x.run = new_run_pac
            if x.run is not None and x.dv is not None and x.p_nombre is not None and x.apellido_pa is not None and x.apellido_ma is not None and x.direccion is not None and x.correo is not None and x.contrasena is not None and y.peso is not None and y.talla is not None:
                if x.run.strip() !='' and x.dv.strip() !='' and x.p_nombre.strip() !='' and x.apellido_pa.strip() !='' and x.apellido_ma.strip() !='' and x.direccion.strip() !='' and x.correo.strip() !='' and x.contrasena.strip() !='' and y.peso.strip() !='' and y.talla.strip() !='': 
                    try:
                        x.save()
                        print("Usuario Paciente Registrado")

                        runpac = request.POST.get('inputRutPaciente')
                        newrun = Usuario.objects.get(run=runpac)
                        y.run_paciente = newrun

                        y.save()
                        print("Paciente 100% Registrado")
                    except:
                        print("Error, RUT Repetido")
                else:
                    print("Error, Campos con caracter de espaciador")
            else:
                print("Error, Campos Nulos")
    else:
        print("Error, Sin retorno del Formulario")
    contexto = {"estados":estados, "comunas":comunas, "generos": generos, "nacionalidades": nacionalidades, "previsiones": previsiones}
    return render(request, "crear_pac.html", contexto)


