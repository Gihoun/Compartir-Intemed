from django.shortcuts import render
from modulo_admin.models import *
from modulo_medico.models import *
from select import select
# Create your views here.


def inicio(request,id):
    paciente = Usuario.objects.get(run=id)
    med = Usuario.objects.filter(id_perfil=2)
    if request.POST:
        ru = request.POST.get("run_medic")
        hor = request.POST.get("fechainput")
        print(hor)

        
        
        if hor is not None and hor != '':
            
            arr_date= hor.split("-")
            print(arr_date)
            agnd = agenda_hora.objects.filter(fecha_hora__year=arr_date[0],fecha_hora__month=arr_date[1],fecha_hora__day=arr_date[2])

            print(agnd)            
            disp = Disponibilidad.objects.filter(run_medico=ru, id_horaD__in=agnd)
        else:
            disp = Disponibilidad.objects.filter(run_medico=ru).select_related('id_horaD')
        contexto = {"paciente": paciente,"medico": med,"disponibilidad":disp}
    else:
        contexto = {"paciente": paciente,"medico": med}
    
    return render(request,"paciente.html", contexto)


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

