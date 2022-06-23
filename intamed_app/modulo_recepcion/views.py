from multiprocessing.sharedctypes import Array
from select import select
from .metodos import *
from django.shortcuts import render
from django.contrib.auth.models import User
from modulo_admin.models import Comuna, EstadoCivil, Genero, Medico, Nacionalidad, Paciente, Usuario, Atencion, Farmaco
from modulo_admin.models import TipoFarmaco, PerfilUsuario, Administrador, Recepcionista, Contrato, TipoContrato, Alergia
from modulo_admin.models import Prevision, TelefonoUsuario, Telefono, DetalleAlergia
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
from django.http import HttpRequest

# Create your views here.

def inicio(request):
    comunas = Comuna.objects.all()
    nacionalidades = Nacionalidad.objects.all()
    estados = EstadoCivil.objects.all()
    generos = Genero.objects.all()
    previsiones = Prevision.objects.all()

    if request.POST:
        x = Usuario()
        y = Paciente()

        new_run_pac = request.POST.get('inputRut')
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

        id_estC = request.POST.get('inputEstadoCivil')
        eestado = EstadoCivil.objects.get(id_estado=id_estC) 
        x.id_estado = eestado

        id_ggen = request.POST.get('inputGenero')
        ggenero = Genero.objects.get(id_genero=id_ggen)
        x.id_genero = ggenero

        id_nnac = request.POST.get('inputNacPac') 
        nnacionalidad = Nacionalidad.objects.get(id_nacionalidad=id_nnac)
        x.id_nacionalidad = nnacionalidad

        id_ccom = request.POST.get('inputComuna')
        ccomuna = Comuna.objects.get(id_comuna=id_ccom)
        x.id_comuna = ccomuna

        perfilu = PerfilUsuario.objects.get(id_perfil=4)
        x.id_perfil = perfilu

        id_previ = request.POST.get('inputPrevision')
        pprev = Prevision.objects.get(id_prevision=id_previ)
        y.id_prevision = pprev

        y.peso = request.POST.get('inputPeso')
        y.talla = request.POST.get('inputTalla')

        try:
            user = Usuario.objects.get(run=new_run_pac)
            print("RUT ya Existe")
            print(user.run)
        except:
            x.run = new_run_pac
            if x.run is not None and x.dv is not None and x.p_nombre is not None and x.apellido_pa is not None and x.apellido_ma is not None and x.direccion is not None and x.correo is not None and x.contrasena is not None and y.peso is not None and y.talla is not None:
                if x.run.strip() !='' and x.dv.strip() !='' and x.p_nombre.strip() !='' and x.apellido_pa.strip() !='' and x.apellido_ma.strip() !='' and x.direccion.strip() !='' and x.correo.strip() !='' and y.peso.strip() !='' and y.talla.strip() !='': 
                    try:
                        x.save()
                        print("Usuario Paciente Registrado")

                        runpac = request.POST.get('inputRut')
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
    contexto = {"estadoCivil":estados, "comuna":comunas, "genero": generos, "nacionalidad": nacionalidades, "prevision": previsiones}
    return render(request, "ingresar_paciente.html", contexto)




def ingresarPago(request):
    return render(request,"ingresar_pago.html")


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
    return render(request, 'buscar_paciente.html', contexto)
 

#Arreglar mañana
def editar_paciente(request,id):
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

    if request.POST:
        ## CAMPOS INCLUSIVOS DE USUARIO
        p_nom = request.POST.get("inputPNom")
        s_nom = request.POST.get("inputSNom")
        nom_soc = request.POST.get("inputNomSoc")
        ap_pa = request.POST.get("inputAp")
        ap_ma = request.POST.get("inputAM")
        com_p = request.POST.get("inputComuna")
        dir_p = request.POST.get("inputDir")
        correo_p = request.POST.get("inputCorreo")
        nac_p = request.POST.get("inputNac")
        fec_nacP = request.POST.get("fechaNac")
        est_p = request.POST.get("inputEstadoCivil")
        gen_p = request.POST.get("inputGenero")
        
        ## CAMPOS EXCLUSIVOS DE PACIENTE
        prev = request.POST.get("inputPrevi")
        
        
        flag , userr = editar_usuario_gral(id, p_nom, s_nom, nom_soc, ap_pa, ap_ma, com_p, dir_p, correo_p, nac_p, fec_nacP, est_p, gen_p)
        if flag:
            try:##FALTA ALERGIAS Y TELEFONOS
                prevP = Prevision.objects.get(nombre_prevision=prev)
                paciente_real.id_prevision = prevP
                paciente_real.save()

                mensaje="paciente guardado exitosamente"
                contexto = {"paciente": userr, "prevision": prevision, "telefonos": num_tel, "cantidad": cant_tel,
                "comuna": comunas, "nacionalidad": nacionalidades, "estado": estados, "genero": generos}
            except:
                mensaje="usuario base guardado problemas en paciente"
        else:
            mensaje="problemas al guardar usuario base"
    
    logger.warning(mensaje)
   

    contexto = {"paciente": paciente, "prevision": prevision, "telefonos": num_tel, "cantidad": cant_tel,
                "comuna": comunas, "nacionalidad": nacionalidades, "estado": estados, "genero": generos}
   
    return render(request, 'editar_paciente.html',contexto)



def anularHora(request):
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
    return render(request, "anular_hora.html", contexto)


def anularHora(request):
    
    return render(request, 'atenciones.html')