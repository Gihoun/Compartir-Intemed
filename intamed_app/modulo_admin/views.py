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

def edit_paciente(request,id):
    prevision = Prevision.objects.all()
    tel_users = TelefonoUsuario.objects.filter(run_usuario=id).values_list('id_telefono', flat=True)
       
    num_tel = Telefono.objects.all().filter(id_telefono__in=tel_users).values_list('num_telefono', flat=True)
    cant_tel = tel_users.count() 
    cant = num_tel.count()
    
    paciente = Usuario.objects.get(run=id)
    comunas = Comuna.objects.all()
    nacionalidades = Nacionalidad.objects.all()
    estados = EstadoCivil.objects.all()
    generos = Genero.objects.all()

    todo_alergias = Alergia.objects.all()
    aler_user = DetalleAlergia.objects.filter(run_paciente=id).values_list('id_alergia',flat=True)
    alergias = Alergia.objects.all().filter(id_alergia__in=aler_user).values_list('nombre_alergia', flat=True)

    contexto = {"paciente": paciente, "prevision": prevision, "telefonos": num_tel, "cantidad": cant_tel,
                "comuna": comunas, "nacionalidad": nacionalidades, "estado": estados, "genero": generos, "alergias": alergias,"alers":todo_alergias}
    ##if request.POST:
    ##    print("holi")
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
                    flag=True
                    mensaje="Perfil de Usuario Modificado con Éxito"
            else:
                mensaje="Edición de Perfil Inválida"
                flag=False 
            contexto = {"perfil": perfil,"mensaje": mensaje}
            messages.info(request, mensaje)
            logger.warning(mensaje)
        except:
            flag=False
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
    tel_users = TelefonoUsuario.objects.filter(run_usuario=id).values_list('id_telefono', flat=True)
    cant_tel = tel_users.count()    
    num_tel = Telefono.objects.all().filter(id_telefono__in=tel_users).values_list('num_telefono', flat=True)
    comunas= Comuna.objects.all()
    nacionalidades = Nacionalidad.objects.all()
    estados = EstadoCivil.objects.all()
    generos = Genero.objects.all()

    mensaje=''
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
        comuna = Comuna.objects.get(nombre_comuna=com_colab)
        nacionalidad = Nacionalidad.objects.get(nombre_nac=nac_colab)
        estado = EstadoCivil.objects.get(nombre_estado=est_colab)
        genero = Genero.objects.get(nombre_genero=gen_colab)

        # Campos a Modificar propios de la Tabla Administrador, Médico y Recepcionista:
        if colab.id_perfil == 1:
            fec_ing_colab = request.POST.get("inputFechaIngreso")
            sueldo = request.POST.get("inputSueldo")
        elif colab.id_perfil == 2:
            fec_ing_colab = request.POST.get("inputFechaIngreso")
            sueldo = request.POST.get("inputSueldo")
            reg_hrs = request.POST.get("inputRegimenHrs")
        elif colab.id_perfil == 3:
            fec_ing_colab = request.POST.get("inputFechaIngreso")
            sueldo = request.POST.get("inputSueldo")        

        # Proceso de Modificación de los Campos
        try:
            colab = Usuario.objects.get(run=id)
            telefono = Telefono.objects.get(id_telefono__in=tel_users)
            admin = Administrador.objects.get(run_admin=id)
            medico = Medico.objects.get(run_medico=id)
            recep = Recepcionista.objects.get(run_recepcionista=id)

            if colab.id_perfil == 1:
                admin.fecha_ingreso = fec_ing_colab
                admin.sueldo = sueldo
            elif colab.id_perfil == 2:
                medico.fecha_ingreso = fec_ing_colab
                medico.sueldo = sueldo
                medico.regimen_hrs = reg_hrs
            elif colab.id_perfil == 3:
                recep.fec_ing_colab = fec_ing_colab
                recep.sueldo = sueldo

            colab.fecha_nac = fec_nac_colab
            colab.id_estado = estado
            colab.id_genero = genero
            colab.id_nacionalidad = nacionalidad
            colab.id_comuna = comuna
            telefono.num_telefono = tel_colab
            #logger.warning(tel_users) 
            
            if colab.id_perfil == 1 or colab.id_perfil == 3:
                if p_nom is not None and s_nom is not None and ap_pa is not None and ap_ma is not None and dir_colab is not None and correo_colab is not None and sueldo is not None:
                    if p_nom.strip() !='' and s_nom.strip() !='' and ap_pa.strip() !='' and ap_ma.strip() !='' and dir_colab.strip() !='' and correo_colab.strip() !='' and sueldo.strip() !='':
                        colab.p_nombre = p_nom
                        colab.nombre_social = nom_soc
                        colab.s_nombre = s_nom
                        colab.apellido_pa = ap_pa
                        colab.apellido_ma = ap_ma
                        colab.direccion = dir_colab
                        colab.correo = correo_colab
                        if colab.id_perfil == 1:
                            admin.sueldo = sueldo
                            admin.save()
                        elif colab.id_perfil == 3:
                            recep.sueldo = sueldo
                            recep.save()
                        colab.save()
                        telefono.save()
                        flag=True
                        mensaje="Colaborador Modificado con Éxito"
                else:
                    mensaje="Campos No Válidos"
                    flag=False 
                messages.info(request, mensaje)
                logger.warning(mensaje)
                contexto = {"colab": colab, "telefonos": num_tel, "cantidad": cant_tel, "comuna": comunas, 
                        "nacionalidad":nacionalidades, "estado":estados, "genero":generos, "mensaje": mensaje}

            if colab.id_perfil == 2:
                if p_nom is not None and s_nom is not None and ap_pa is not None and ap_ma is not None and dir_colab is not None and correo_colab is not None and sueldo is not None and reg_hrs is not None:
                    if p_nom.strip() !='' and s_nom.strip() !='' and ap_pa.strip() !='' and ap_ma.strip() !='' and dir_colab.strip() !='' and correo_colab.strip() !='' and sueldo.strip() !='' and reg_hrs.strip() !='':
                        colab.p_nombre = p_nom
                        colab.nombre_social = nom_soc
                        colab.s_nombre = s_nom
                        colab.apellido_pa = ap_pa
                        colab.apellido_ma = ap_ma
                        colab.direccion = dir_colab
                        colab.correo = correo_colab
                        medico.regimen_hrs = reg_hrs
                        colab.save()
                        telefono.save()
                        medico.save()
                        flag=True
                        mensaje="Colaborador Modificado con Éxito"
                else:
                    mensaje="Campos No Válidos"
                    flag=False 
                messages.info(request, mensaje)
                logger.warning(mensaje)
                contexto = {"colab": colab, "telefonos": num_tel, "cantidad": cant_tel, "comuna": comunas, 
                        "nacionalidad":nacionalidades, "estado":estados, "genero":generos, "mensaje": mensaje}
            
        except:
            flag=False
            mensaje="Colaborador No Modificado"
            messages.info(request, mensaje)
            logger.warning(mensaje)
            contexto = {"colab": colab, "telefonos": num_tel, "cantidad": cant_tel, "comuna": comunas, 
                        "nacionalidad":nacionalidades, "estado":estados, "genero":generos,"mensaje": colab}
    else:
        contexto = {"colab": colab, "telefonos": num_tel, "cantidad": cant_tel, "comuna": comunas, 
                    "nacionalidad":nacionalidades, "estado":estados, "genero":generos, "mensaje": mensaje}
    return render(request, 'edit_usuario.html', contexto)