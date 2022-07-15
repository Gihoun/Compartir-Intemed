from multiprocessing.sharedctypes import Array
from select import select
from .metodos import *
from django.shortcuts import render
from django.contrib.auth.models import User
from modulo_medico.models import *
from modulo_medico.views import insert_DetAtencio,genpdf_boleta
from modulo_admin.models import Comuna, EstadoCivil, Genero, Medico, Nacionalidad, Paciente, Usuario, Atencion, Farmaco
from modulo_admin.models import TipoFarmaco, PerfilUsuario, Administrador, Recepcionista, Contrato, TipoContrato, Alergia
from modulo_admin.models import Prevision, TelefonoUsuario, Telefono, DetalleAlergia, DetalleAtencion, Boleta
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
from datetime import datetime
from django.http import HttpRequest
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.shortcuts import redirect
from django.core.mail import send_mail

# Create your views here.
@login_required()
def inicio(request):
    logueado = request.user
    run_re = logueado.usuario_django.run_django
    usu_re = Usuario.objects.get(run=run_re)
    contexto = {"recep":usu_re}
    return render(request, "index_recepcion.html",contexto)

@login_required()
def ingresarPac(request):
    logueado = request.user
    run_re = logueado.usuario_django.run_django
    usu_re = Usuario.objects.get(run=run_re)
    
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
        x.fecha_nac = request.POST.get('inputNac')  
        x.contrasena = "temporal123"

        id_estC = request.POST.get('inputEstadoCivil')
        eestado = EstadoCivil.objects.get(id_estado=id_estC) 
        x.id_estado = eestado
        print(f'id estado {x.id_estado}')

        id_ggen = request.POST.get('inputGenero')
        ggenero = Genero.objects.get(id_genero=id_ggen)
        x.id_genero = ggenero
        print(f'id genero {x.id_genero}')

        id_nnac = request.POST.get('inputNacPac') 
        print(f'id nacionalidad  {id_nnac}')
        nnacionalidad = Nacionalidad.objects.get(nombre_nac=id_nnac)
        x.id_nacionalidad = nnacionalidad

        id_ccom = request.POST.get('inputComuna')
        ccomuna = Comuna.objects.get(id_comuna=id_ccom)
        x.id_comuna = ccomuna
        print(f'id comuna {x.id_comuna}')
        perfilu = PerfilUsuario.objects.get(id_perfil=4)
        x.id_perfil = perfilu

        id_previ = request.POST.get('inputPrevision')
        pprev = Prevision.objects.get(id_prevision=id_previ)
        y.id_prevision = pprev
        print(f'id prev {y.id_prevision}')

        y.peso = request.POST.get('inputPeso')
        y.talla = request.POST.get('inputTalla')

        try:
            user = Usuario.objects.get(run=new_run_pac)
            print("RUT ya Existe")
            print(user.run)
        except:
            x.run = new_run_pac
            if x.run is not None and x.dv is not None and x.p_nombre is not None and x.apellido_pa is not None and x.apellido_ma is not None and x.direccion is not None and x.correo is not None and x.contrasena is not None:# and y.peso is not None and y.talla is not None:
                if x.run.strip() !='' and x.dv.strip() !='' and x.p_nombre.strip() !='' and x.apellido_pa.strip() !='' and x.apellido_ma.strip() !='' and x.direccion.strip() !='' and x.correo.strip() !='':# and y.peso.strip() !='' and y.talla.strip() !='': 
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
    contexto = {"estadoCivil":estados, "comuna":comunas, "genero": generos, "nacionalidad": nacionalidades, "prevision": previsiones,"recep":usu_re}
    return render(request, "ingresar_paciente.html", contexto)



@login_required()
def ingresarPago(request):
    prev = Prevision.objects.all()   
    logueado = request.user
    run_re = logueado.usuario_django.run_django
    usu_re = Usuario.objects.get(run=run_re)
   
    if request.POST:
        rp = request.POST.get('runp')        
        inpvalue = request.POST.get('inpval')
        id_dispo = request.POST.get('id_dispon')
        print(f'input value {inpvalue} id disp {id_dispo}')
        if rp is not None: 
            if rp.strip()!= '':
                runf = rp
                try:
                    obj_pac = Usuario.objects.get(run=runf)
                    detalle = det_agenda.objects.filter(run_pac=runf)
                    tomadas =detalle.values_list("idda")
                    age = Disponibilidad.objects.filter(id_disp__in=tomadas).select_related('id_horaD')
                except:
                    runf = 0
                    obj_pac = None
                    age = None
            else:
                runf = 0
                obj_pac = None
                age = None
        else:
            runf = 0
            obj_pac = None
            age = None
        
        if len(inpvalue) != 0 and rp is not None:
            
            print("SE GENERARA LA BOLETA")
            pac = Paciente.objects.get(run_paciente=rp)
            disp = Disponibilidad.objects.get(id_disp=id_dispo)
            print(f'id PACIENTE {runf}')
            med = disp.run_medico_id
            
            try:
                # generar atencion vacia 
                fe = datetime.now()
                ate_new= Atencion()
                id_at = Atencion.objects.last().id_atencion
                
                ate_new.id_atencion = id_at+7
                ate_new.fecha_atencion = fe

                print(ate_new.id_atencion)
                
                ate_new.save()
                print("ATENCION NUEVA GUARDADA")

                insert_DetAtencio(rp, ate_new.id_atencion)
                
                print("DETALLE ATENCION GENERADO")
                
                
                f_boleta = fe.strftime('%Y-%m-%d')

                print(f'id atencion {ate_new.id_atencion} valor {inpvalue} fecha {f_boleta}')
                newB = Boleta()

                newB.id_atencion = ate_new
                newB.fecha_boleta = f_boleta
                newB.monto_pago = inpvalue
                try:
                    newB.save()  ##just for testing
                    dat = str(ate_new.id_atencion) + '-' + str(runf) + '-'+ str(med)
                    print(f'BOLETA INGRESADA CON EXITO {ate_new.id_atencion}')
                    #response = redirect('modulo_recepcion:genpdf',id=dat)
                    return genpdf_boleta(request,dat)             
                except:
                    bol = Boleta.objects.get(id_atencion=ate_new)
                    print(" YA SE REALIZO EL PAGO POR ESTA ATENCION")
            except:
                print(" EL PACIENTE NO TIENE ATENCION GENERADA")

        contexto={"pac": obj_pac,"prevision": prev,"agenda": age,"recep":usu_re}
        return render(request,"ingresar_pago.html",contexto)

    contexto={"prevision":prev,"recep":usu_re}
   
    return render(request,"ingresar_pago.html",contexto)



@login_required()
def filtro_pacientes(request):
    logueado = request.user
    run_re = logueado.usuario_django.run_django
    usu_re = Usuario.objects.get(run=run_re)
    users_all = Usuario.objects.all()
    if request.POST:
        busqueda = request.POST.get("txbusqueda")
        pac_ret = Usuario.objects.all().select_related('paciente').filter(run__startswith=busqueda, id_perfil=4)
        cant_p = pac_ret.count()
        if cant_p>=1:
            contexto = {"usuarios":pac_ret,"cantidad":cant_p,"recep":usu_re}
        else:
            contexto = {"usuarios":0,"cantidad":0,"recep":usu_re}
    else:
        users_pac = Usuario.objects.all().select_related('paciente').filter(id_perfil=4)[:25]
        userp_cant = users_pac.count()
        contexto = {"usuarios":users_pac,"cantidad":userp_cant,"recep":usu_re}
    return render(request, 'buscar_paciente.html', contexto)
 

#Arreglar mañana
@login_required()
def editar_paciente(request,id):
    logger = logging.getLogger(__name__)
    logueado = request.user
    run_re = logueado.usuario_django.run_django
    usu_re = Usuario.objects.get(run=run_re)
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
                "comuna": comunas, "nacionalidad": nacionalidades, "estado": estados, "genero": generos,"recep":usu_re}
            except:
                mensaje="usuario base guardado problemas en paciente"
        else:
            mensaje="problemas al guardar usuario base"
    
    logger.warning(mensaje)
   

    contexto = {"paciente": paciente, "prevision": prevision, "telefonos": num_tel, "cantidad": cant_tel,
                "comuna": comunas, "nacionalidad": nacionalidades, "estado": estados, "genero": generos,"recep":usu_re}
   
    return render(request, 'editar_paciente.html',contexto)



def anularHora(request):
    users_all = Usuario.objects.all()
    logueado = request.user
    run_re = logueado.usuario_django.run_django
    usu_re = Usuario.objects.get(run=run_re)
    med = Usuario.objects.filter(id_perfil=2)

   
    det_age = det_agenda.objects.all()
    tomadas =det_age.values_list("idda")

    age = Disponibilidad.objects.filter(id_disp__in=tomadas)

    contexto = {"medico": med,"agenda":age,"det_age":det_age,"recep":usu_re}

    if request.POST:
        idh= request.POST.get("id_hora")
        id_pac = request.POST.get("id_pac")
        fecha_s = request.POST.get("fechainput")
        #paciente = Usuario.objects.get(run=id_pac)
        if idh is not None:
            deta = det_agenda.objects.get(idda=idh)
            deta.delete()
            print(f"la hora que se elimino {idh}")
            send_mail(
                    'Subject here',
                    'Hora eliminada.',
                    'intemed.clinica@gmail.com',
                    ['an.verdugom@duocuc.cl'],
                    fail_silently=False,
            )
        elif fecha_s is not None and fecha_s.strip() != '':
            print(fecha_s)
            
            
            det_h = agenda_hora.objects.filter(fecha_hora__date=fecha_s)
            dispo= Disponibilidad.objects.filter(id_horaD__in=det_h,id_disp__in=tomadas)
            contexto = {"medico": med,"agenda":dispo,"det_age":det_age,"recep":usu_re}
            
            #paciente = Usuario.objects.get(run=id_pac)
    
    return render(request, "anular_hora.html", contexto)

def tomar_hora(request):
    med = Usuario.objects.filter(id_perfil=2)
    tom = det_agenda.objects.values_list("idda")
    disp = Disponibilidad.objects.select_related('id_horaD').exclude(id_disp__in=tom)

    logueado = request.user
    run_re = logueado.usuario_django.run_django
    usu_re = Usuario.objects.get(run=run_re)
    
    if request.POST:
        runm = request.POST.get("run_medic")
        rut = request.POST.get("inputRut")
        dat = request.POST.get("fechainput")
        sel_hora = request.POST.get("hor_sel")
        print(sel_hora)

        if sel_hora is not None and sel_hora != '':
            print(f'el valor de selhora {sel_hora}')
            di = Disponibilidad.objects.get(id_disp=sel_hora)
            pac = Paciente.objects.get(run_paciente=rut)
            userP =  Usuario.objects.get(run=rut)
            
            try:
                test_det = det_agenda.objects.get(idd=sel_hora)
                print(f'hora NO DISPONIBLE')
            except:
                new_agenda = det_agenda()
                new_agenda.idd = di
                new_agenda.run_pac = pac
                new_agenda.idda = sel_hora
                new_agenda.save()
                print(f'hora agendada con exito')
                send_mail(
                    'Subject here',
                    'Hora Agendada ',
                    'intemed.clinica@gmail.com',
                    ['an.verdugom@duocuc.cl'],
                    fail_silently=False,
                )
        if dat is not None and dat != '':
            
            arr_date= dat.split("-")
            print(arr_date)
            agnd = agenda_hora.objects.filter(fecha_hora__year=arr_date[0],fecha_hora__month=arr_date[1],fecha_hora__day=arr_date[2])

            print(agnd)            
            disp = Disponibilidad.objects.filter(run_medico=runm, id_horaD__in=agnd)
        else:

            disp = Disponibilidad.objects.filter(run_medico=runm).select_related('id_horaD').exclude(id_disp__in=tom)

    
    contexto = {"medico":med,"disponibilidad":disp,"recep":usu_re}
    return render(request,'tomar_hora.html',contexto)

