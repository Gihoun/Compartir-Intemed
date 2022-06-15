#FUNCION PARA GUADAR HACIA TABLA USUARIO------------------
from .models import *

def editar_usuario_gral(id_user,p_nom,s_nom,nom_soc,ap,am,com,dire,correo,nac,fech,est,gen):
    # recoge un request
    usr = Usuario.objects.get(run=id_user)
    comuna = Comuna.objects.get(nombre_comuna=com)
    nacionalidad = Nacionalidad.objects.get(nombre_nac=nac)
    estado = EstadoCivil.objects.get(nombre_estado=est)
    genero = Genero.objects.get(nombre_genero=gen)
    if p_nom is not None and ap is not None and am is not None and dire is not None and correo is not None:
        if p_nom.strip() !='' and ap.strip() !='' and am.strip() !='' and dire.strip() !='' and correo.strip() !='':
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
        newT = Telefono.objects.create(num_telefono=new_tel,id_telefono=id_obj,id_tipo_tel=tip_tel)
        tel_obj = TelefonoUsuario.objects.create(run_usuario=usr,id_telefono=newT)
        newT.save()
        tel_obj.save()
        
        msg="Exito agregando nuevo telefono"
        return msg 
    except:   
        msg="error agregando nuevo telefono"
        return msg