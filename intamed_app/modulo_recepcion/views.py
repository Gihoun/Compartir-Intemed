from multiprocessing.sharedctypes import Array
from select import select
from .metodos import *
from django.shortcuts import render
from django.contrib.auth.models import User
from modulo_medico.models import *
from modulo_admin.models import Comuna, EstadoCivil, Genero, Medico, Nacionalidad, Paciente, Usuario, Atencion, Farmaco
from modulo_admin.models import TipoFarmaco, PerfilUsuario, Administrador, Recepcionista, Contrato, TipoContrato, Alergia
from modulo_admin.models import Prevision, TelefonoUsuario, Telefono, DetalleAlergia, DetalleAtencion
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
    prev = Prevision.objects.all()
    
    if request.POST:
        rp = request.POST.get('runp')
        fdr_uno = request.POST.get('flexRadioDefault')
        print(f' flex radio button value {fdr_uno}')
        inpvalue = request.POST.get('inpval')
        
        if rp is not None: 
            if rp.strip()!= '':
                runf = rp
                obj_pac = Usuario.objects.get(run=runf)
            else:
                runf = 0
                obj_pac = None
        else:
            runf = 0
            obj_pac = None
        
        if fdr_uno is not None and len(inpvalue) != 0 :
            arr_2=[]
            print("SE GENERARA LA BOLETA")
            pac = Paciente.objects.get(run_paciente=rp)
            
            
            print(f'id PACIENTE {runf}')
            det_at_selected = DetalleAtencion.objects.filter(run_paciente=runf)
            id_at= list(det_at_selected.values_list("id_atencion"))
            print(id_at)
            if len(id_at) > 0:
                # MANDAR POR PANTALLA SWAL FECHA HORA ID Y PERSONA para confirmar ANTES DEL POST
                for f in id_at:
                    arr_2.append(f[0])
                ate= Atencion.objects.filter(id_atencion__in=arr_2).last()
                fe = datetime.now()
                f_boleta = fe.strftime('%Y-%m-%d')

                print(f'id atencion {ate} valor {inpvalue} fecha {f_boleta}')
                new = Boleta()

                new.id_atencion = ate
                new.fecha_boleta = f_boleta
                new.monto_pago = inpvalue
                try:
                    bol = Boleta.objects.get(id_atencion=ate)
                    print(" YA SE REALIZO EL PAGO POR ESTA ATENCION")
                except:
                    new.save()
                    dat = str(ate.id_atencion) + '-' + str(runf)
                    print(f'BOLETA INGRESADA CON EXITO {ate.id_atencion}')
                    response = redirect('genpdf',id=dat)
                    return response
            else:
                print(" EL PACIENTE NO TIENE ATENCION GENERADA")

        contexto={"pac": obj_pac,"prevision": prev}
        return render(request,"ingresar_pago.html",contexto)
    else:
        contexto={"prevision":prev}
        

    return render(request,"ingresar_pago.html",contexto)
def genpdf_boleta(request,id):
    arr_1= id.split('-')

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    bol = Boleta.objects.get(id_atencion=arr_1[0])
    uss = Usuario.objects.get(run=arr_1[1])
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    valor = bol.monto_pago
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    img_file = "./modulo_recepcion/static/img/clipart2045091.png"
    
    x_start = 0
    y_start = 0
    p.drawImage(img_file, x_start, y_start, width=120, preserveAspectRatio=True, mask='auto')
    p.drawString(100, 600, f"Boleta generada por la atencion: {arr_1[0]}")
    p.drawString(100, 580, f"por un valor de {valor}")
    p.drawString(100, 560, f"Pago realizado a nombre de: {uss.p_nombre} {uss.s_nombre}")
    filname = 'boleta' + str(id) + '.pdf'
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=filname)


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
    
    med = Usuario.objects.filter(id_perfil=2)

    #detalle = det_agenda.objects.filter(run_pac=id)
    #tom =detalle.values_list("idda")
    #print(tom)

    if request.POST:
        idh= request.POST.get("id_hora")
        id_pac = request.POST.get("id_pac")
        paciente = Usuario.objects.get(run=id_pac)
    
        deta = det_agenda.objects.get(idda=idh)
        deta.delete()
        print(f"la hora que se eliminada {idh}")
        send_mail(
                'Subject here',
                'Here is the message.',
                'andrea.verdugomunoz@gmail.com',
                ['an.verdugom@duocuc.cl'],
                fail_silently=False,
        )
    #fe = datetime.now()
    #f_dia = fe.strftime('%Y-%m-%d')
   
    #det_h = agenda_hora.objects.filter(fecha_hora__date=f_dia)


    #age = Disponibilidad.objects.filter(id_disp__in=tom).select_related('id_horaD').select_related('Usuario')
    det_age = det_agenda.objects.all()
    tom =det_age.values_list("idda")
    age = Disponibilidad.objects.filter(id_disp__in=tom)

    contexto = {"medico": med,"agenda":age}
    return render(request, "anular_hora.html", contexto)

