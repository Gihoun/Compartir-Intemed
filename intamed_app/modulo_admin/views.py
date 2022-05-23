from multiprocessing.sharedctypes import Array
from select import select
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Medico, Paciente, Usuario, Atencion, Farmaco, Prevision, TelefonoUsuario, Telefono
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required,permission_required
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.db.models import Count
import requests
import logging
from django.http import JsonResponse

# Create your views here.
def administrator(request):
    #Dash por defecto
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
    users_all = Usuario.objects.all()[:25]
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
        #pac_ret = Paciente.objects.all().select_related('run_paciente').filter(run_paciente_id__startswith=busqueda)
        cant_p = pac_ret.count()
        if cant_p>=1:
            #user_ret = Usuario.objects.filter(run__startswith=busqueda)
            contexto = {"usuarios":pac_ret,"cantidad":cant_p}
        else:
            contexto = {"usuarios":0,"cantidad":0}
    else:
        users_pac = Usuario.objects.all().select_related('paciente').filter(id_perfil=4)[:25]
        userp_cant = users_pac.count()
        contexto = {"usuarios":users_pac,"cantidad":userp_cant}
    return render(request, 'pacientes_s.html', contexto)


def edit_paciente(request,id):
    tel = []
    prevision = Prevision.objects.all()
    tel_users = TelefonoUsuario.objects.filter(run_usuario=id).values_list('id_telefono', flat=True)
    cant_tel = tel_users.count()    
    num_tel = Telefono.objects.all().filter(id_telefono__in=tel_users).values_list('num_telefono', flat=True)
    cant = num_tel.count()
    paciente = Usuario.objects.get(run=id)
    contexto = {"paciente": paciente, "prevision": prevision, "telefonos": num_tel, "cantidad": cant_tel}
    if request.POST:
        print("holi")
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

