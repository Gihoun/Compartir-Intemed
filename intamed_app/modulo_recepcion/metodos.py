from modulo_admin.models import *

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