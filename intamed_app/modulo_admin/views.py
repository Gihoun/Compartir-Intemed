from multiprocessing.sharedctypes import Array
from select import select
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Comuna, DetalleAtencion, EstadoCivil, Genero, Medico, Nacionalidad, Paciente, Usuario
from .models import TipoFarmaco, PerfilUsuario, Administrador, Recepcionista, Contrato, TipoContrato, Alergia
from .models import Prevision, TelefonoUsuario, Telefono, DetalleAlergia, TipoTelefono, Atencion, Farmaco
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
        contexto1 = {"cant":users_all,
                "ene":ate_mes1,
                "feb":ate_mes2,
                "mar":ate_mes3,
                "abr":ate_mes4,
                "may":ate_mes5,
                "jun":ate_mes6,
                "jul":ate_mes7
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
        contexto = {"cant":users_all,
                    "ene":ate_mes1,
                    "feb":ate_mes2,
                    "mar":ate_mes3,
                    "abr":ate_mes4,
                    "may":ate_mes5,
                    "jun":ate_mes6,
                    "jul":ate_mes7
                    }
    return render(request,"administrator.html",contexto)

def filtro_usuarios(request):
    arr_id=[1,2,3]
    users_all = Usuario.objects.filter(id_perfil__in = arr_id)
    users_cant = users_all.count()
    if request.POST:
        busqueda = request.POST.get("txbusqueda")
        users_ret = Usuario.objects.filter(run__startswith=busqueda, id_perfil__in = arr_id)
        users_cant = users_ret.count()
        contexto = {"usuarios":users_ret,"cantidad":users_cant}
    else:
        users_all = Usuario.objects.all().filter(id_perfil__in = arr_id)
        contexto = {"usuarios":users_all,"cantidad":users_cant}
    return render(request, 'usuarios_s.html', contexto)

def filtro_pacientes(request):
    users_all = Usuario.objects.all()
    if request.POST:
        busqueda = request.POST.get("txbusqueda")
        pac_ret = Usuario.objects.all().select_related('paciente').filter(run__startswith=busqueda, id_perfil=4)
        cant_p = pac_ret.count()
        if cant_p>=1:
            contexto = {"usuarios":pac_ret,"cantidad":cant_p}
        else:
            contexto = {"usuarios":0,"cantidad":0}
    else:
        users_pac = Usuario.objects.all().select_related('paciente').filter(id_perfil=4)[:25]
        userp_cant = users_pac.count()
        contexto = {"usuarios":users_pac,"cantidad":userp_cant}
    return render(request, 'pacientes_s.html', contexto)

#FUNCION PARA GUADAR HACIA TABLA USUARIO------------------
def editar_usuario_gral(id_user,p_nom,s_nom,nom_soc,ap,am,com,dire,correo,nac,fech,est,gen):
    # recoge un request
    usr = Usuario.objects.get(run=id_user)
    comuna = Comuna.objects.get(nombre_comuna=com)
    nacionalidad = Nacionalidad.objects.get(nombre_nac=nac)
    estado = EstadoCivil.objects.get(nombre_estado=est)
    genero = Genero.objects.get(nombre_genero=gen)
    if p_nom is not None and s_nom is not None and ap is not None and am is not None and dire is not None and correo is not None:
        if p_nom.strip() !='' and s_nom.strip() !='' and ap.strip() !='' and am.strip() !='' and dire.strip() !='' and correo.strip() !='':
            try:
                usr.p_nombre = p_nom
                usr.s_nombre = s_nom
                usr.nombre_social = nom_soc
                usr.apellido_pa = ap
                usr.apellido_ma = am
                usr.direccion = dire
                usr.correo = correo
                usr.fecha_nac = fech

                usr.id_estado = estado
                usr.id_genero = genero
                usr.id_nacionalidad = nacionalidad
                usr.id_comuna = comuna
                usr.save()
                return True , usr
            except:
                return False
    else:
        return False

# LOGICA PARA GUARDAR HACIA TABLA TELEFONO y TELEFONO USUARIO
def save_tel_varios(id_user,arr_new_tel):
    usr=Usuario.objects.get(run=id_user)
    msg=''
    # si ya tiene telefonos
    try:
        tel_users = TelefonoUsuario.objects.filter(run_usuario=id_user).values_list('id_telefono', flat=True) 
        numeros = Telefono.objects.all().filter(id_telefono__in=tel_users).values_list('num_telefono', flat=True)
        obj_num = Telefono.objects.all().filter(id_telefono__in=tel_users)
        cant_tel = tel_users.count()
        if cant_tel != 0:
            for x in range(len(tel_users)):
                if arr_new_tel[x].strip() !='':
                    try:
                        telf = Telefono.objects.get(id_telefono=tel_users[x])
                        telf.num_telefono = arr_new_tel[x]
                        telf.save()
                    except:
                        msg="error alterando telefonos existentes" 
                        return 1 , msg
            msg="Exito telefonos alterados"
            return 2, msg
        else:
            msg="usuario no tiene telefonos registrados"
            return 3 , msg
    #si no tiene telefonos
    except:
        msg="error buscando usuarios y telefono"
        return 3 , msg

def save_tel_unico(id_user,new_tel):
    try:
        usr=Usuario.objects.get(run=id_user)
        id_obj = Telefono.objects.last().id_telefono + 1   
        tip_tel = TipoTelefono.objects.get(id_tipo_tel=6)   
        print(f"id de objeto ultimo mas uno  {id_obj}" )    
        newT = Telefono.objects.create(num_telefono=new_tel,id_telefono=id_obj,id_tipo_tel=tip_tel)
        tel_obj = TelefonoUsuario.objects.create(run_usuario=usr,id_telefono=newT)
        newT.save()
        tel_obj.save()
        
        msg="Exito agregando nuevo telefono"
        return msg 
    except:   
        msg="error agregando nuevo telefono"
        return msg

       

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
        farma_selected = Farmaco.objects.filter(nombre_farmaco__startswith=busqueda)
        farma_cant = farma_selected.count()
        contexto = {"farmacos":farma_selected,"cantidad":farma_cant}
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

        perfil_selected = PerfilUsuario.objects.filter(nombre_perfil__startswith=busqueda)
        perfiles_cant = perfil_selected.count()
        contexto = {"perfiles":perfil_selected,"cantidad":perfiles_cant}
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
            reg_hrs = request.POST.get("inputRegimenHrs")
        elif id_perfil == 3:
            fec_ing_colab = request.POST.get("inputFechaIngreso")
            sueldo = request.POST.get("inputSueldo")        
        # Proceso de Modificación de los Campos
        flag ,usr = editar_usuario_gral(id, p_nom, s_nom, nom_soc, ap_pa, ap_ma, com_colab, dir_colab, correo_colab, nac_colab, fec_nac_colab, est_colab, gen_colab)
        if flag:
            # despues del registro del usuario base
            # se aplica logica para guardar su telefono en el caso de que tenga o que no tenga
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
                    medico = Medico.objects.get(run_medico=id)
                    medico.fecha_ingreso = fec_ing_colab
                    medico.sueldo = sueldo
                    medico.regimen_hrs = reg_hrs
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

def vista_atenciones(request):
    atenciones = Atencion.objects.all()
    atenciones_cant = atenciones.count()
    if request.POST:
        busqueda = request.POST.get("txbusqueda")
        atencion_selected = Atencion.objects.filter(id_atencion__startswith=busqueda)
        #det_at_selected = DetalleAtencion.objects.filter(id_atencion__startswith=busqueda)
        atenciones_cant = atencion_selected.count()
        contexto = {"atencion":atencion_selected,"cantidad":atenciones_cant} #,"detalle":det_at_selected}
    else:
        contexto = {"atencion":atenciones,"cantidad":atenciones_cant} #,"detalle":det_at_selected}
    return render(request, 'atenciones.html', contexto)