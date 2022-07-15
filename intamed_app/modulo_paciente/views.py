from django.shortcuts import render
from modulo_admin.models import *
from modulo_medico.models import *
from select import select
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.


@login_required()
def inicio(request,id):
    paciente = Usuario.objects.get(run=id)
    med = Usuario.objects.filter(id_perfil=2)
    
    tom = det_agenda.objects.values_list("idda")
       
    tom_us = det_agenda.objects.filter(run_pac=id)
   
    age = Disponibilidad.objects.filter(det_agenda__in=tom_us)

    if request.POST:
        ru = request.POST.get("run_medic")
        dat = request.POST.get("fechainput")
        sel_hora = request.POST.get("hor_sel")
        print(sel_hora)

        if sel_hora is not None and sel_hora != '':
            print(f'el valor de selhora {sel_hora}')
            di = Disponibilidad.objects.get(id_disp=sel_hora)
            pac = Paciente.objects.get(run_paciente=id)
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

        if dat is not None and dat != '':
            
            arr_date= dat.split("-")
            print(arr_date)
            agnd = agenda_hora.objects.filter(fecha_hora__year=arr_date[0],fecha_hora__month=arr_date[1],fecha_hora__day=arr_date[2])

            print(agnd)            
            disp = Disponibilidad.objects.filter(run_medico=ru, id_horaD__in=agnd)
        else:

            disp = Disponibilidad.objects.filter(run_medico=ru).select_related('id_horaD').exclude(id_disp__in=tom)

        contexto = {"paciente": paciente,"medico": med,"disponibilidad":disp, "agenda" : age}
    else:
        print(f'esto es el objeto {age}')
        contexto = {"paciente": paciente,"medico": med,"agenda" : age}
    
    return render(request,"paciente.html", contexto)


@login_required()
def anular_hr(request,id):
    paciente = Usuario.objects.get(run=id)
    med = Usuario.objects.filter(id_perfil=2)
    detalle = det_agenda.objects.filter(run_pac=id)
    tom =detalle.values_list("idda")
    print(tom)

    if request.POST:
        idh= request.POST.get("id_hora")

        
        deta = det_agenda.objects.get(idda=idh)
        deta.delete()
        print(f"la hora que se eliminada {idh}")
        send_mail(
                'Subject here',
                'Hora Anulada '+paciente.p_nombre,
                'intemed.clinica@gmail.com',
                ['an.verdugom@duocuc.cl'],
                fail_silently=False,
        )
        

    age = Disponibilidad.objects.filter(id_disp__in=tom).select_related('id_horaD').select_related('Usuario')
    
    contexto = {"paciente": paciente,"medico": med,"agenda":age}
    
    return render(request,"anularhr_paciente.html", contexto)


@login_required()
def mi_cuenta(request, id):
    
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

       
    
   

    contexto = {"paciente": paciente, "prevision": prevision, "telefonos": num_tel, "cantidad": cant_tel,
                "comuna": comunas, "nacionalidad": nacionalidades, "estado": estados, "genero": generos, "alergias": alergias,"alers":todo_alergias}
    return render(request,"micuenta.html",contexto)
