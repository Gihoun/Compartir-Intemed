# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from math import trunc
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import date
from datetime import datetime 


class Usuario(models.Model):
    
    run = models.BigIntegerField(primary_key=True)
    dv = models.CharField(max_length=1)
    p_nombre = models.CharField(max_length=100)
    nombre_social = models.CharField(max_length=100, blank=True, null=True)
    s_nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido_pa = models.CharField(max_length=100)
    apellido_ma = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    fecha_nac = models.DateField()
    contrasena = models.CharField(max_length=32)
    id_estado = models.ForeignKey('EstadoCivil', models.DO_NOTHING, db_column='id_estado')
    id_genero = models.ForeignKey('Genero', models.DO_NOTHING, db_column='id_genero')
    id_nacionalidad = models.ForeignKey('Nacionalidad', models.DO_NOTHING, db_column='id_nacionalidad')
    id_comuna = models.ForeignKey('Comuna', models.DO_NOTHING, db_column='id_comuna')
    id_perfil = models.ForeignKey('PerfilUsuario', models.DO_NOTHING, db_column='id_perfil')
   
  
    @property
    def edad_actual(self):
        if self.fecha_nac:
            # Obtener fecha de hoy
            today = date.today()
            # Calcular Edad
            age = today.year - self.fecha_nac.year - (
                    (today.month, today.day) < (self.fecha_nac.month, self.fecha_nac.day))
            return age

        # Si no tiene fecha su edad es 0
        return 0
    
    class Meta:
        
        managed = True
        db_table = 'usuario'

class Administrador(models.Model):
    run_admin = models.OneToOneField('Usuario', on_delete=models.CASCADE, db_column='run_admin', primary_key=True)
    fecha_ingreso = models.DateField()
    sueldo = models.BigIntegerField()
    id_contrato = models.ForeignKey('Contrato', models.DO_NOTHING, db_column='id_contrato')

    class Meta:
        managed = False
        db_table = 'administrador'


class Agenda(models.Model):
    id_agenda = models.BigIntegerField(primary_key=True)
    dia = models.BigIntegerField()
    mes = models.BigIntegerField()
    anio = models.BigIntegerField()
    hora = models.TextField()  # This field type is a guess.
    

    class Meta:
        managed = False
        db_table = 'agenda'


class Alergia(models.Model):
    id_alergia = models.BigIntegerField(primary_key=True)
    nombre_alergia = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'alergia'


class Atencion(models.Model):
    id_atencion = models.BigIntegerField(primary_key=True)
    fecha_atencion = models.DateField(default=datetime.now, blank=True, null=True)
    hora_atencion = models.DateTimeField(auto_now_add=True)  # This field type is a guess.
    exploracion_clinica = models.CharField(max_length=500, blank=True, null=True)
    comentario_atencion = models.CharField(max_length=200, blank=True, null=True)
    tratamiento = models.CharField(max_length=500, blank=True, null=True)
    id_diagnostico = models.ForeignKey('Diagnostico', models.DO_NOTHING, db_column='id_diagnostico', blank=True, null=True)
    id_receta = models.ForeignKey('Receta', models.DO_NOTHING, db_column='id_receta', blank=True, null=True)
    id_examen = models.ForeignKey('Examen', models.DO_NOTHING, db_column='id_examen', blank=True, null=True)
    id_licencia = models.ForeignKey('Licencia', models.DO_NOTHING, db_column='id_licencia', blank=True, null=True)
    id_agenda = models.ForeignKey(Agenda, models.DO_NOTHING, db_column='id_agenda', blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'atencion'


class Boleta(models.Model):
    id_atencion = models.OneToOneField(Atencion, models.DO_NOTHING, db_column='id_atencion', primary_key=True)
    fecha_boleta = models.DateField()
    monto_pago = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'boleta'


class Comuna(models.Model):
    id_comuna = models.BigIntegerField(primary_key=True)
    nombre_comuna = models.CharField(max_length=100)
    id_region = models.ForeignKey('Region', models.DO_NOTHING, db_column='id_region')

    class Meta:
        managed = False
        db_table = 'comuna'

class Contrato(models.Model):
    id_contrato = models.BigIntegerField(primary_key=True)
    fecha_ini_cont = models.DateField()
    fecha_ter_cont = models.DateField(blank=True, null=True)
    archivo = models.TextField()
    id_tipo_cont = models.ForeignKey('TipoContrato', models.DO_NOTHING, db_column='id_tipo_cont')

    class Meta:
        managed = False
        db_table = 'contrato'

#class DetalleAgenda(models.Model):
#    id_agenda = models.ForeignKey(Agenda, models.DO_NOTHING, db_column='id_agenda')
#    run_recepcionista = models.ForeignKey('Recepcionista', on_delete=models.CASCADE, db_column='run_recepcionista')
#
#    class Meta:
#        managed = False
#        db_table = 'detalle_agenda'

class DetalleAlergia(models.Model):
    run_paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, db_column='run_paciente')
    id_alergia = models.ForeignKey(Alergia, models.DO_NOTHING, db_column='id_alergia')

    class Meta:
        managed = False
        db_table = 'detalle_alergia'

class DetalleAtencion(models.Model):
    run_paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, db_column='run_paciente', related_name='run')
    id_atencion = models.ForeignKey(Atencion, models.DO_NOTHING, db_column='id_atencion', related_name='ate')

    class Meta:
        managed = False
        db_table = 'detalle_atencion'

class DetalleFarmaco(models.Model):
    id_receta = models.ForeignKey('Receta', models.DO_NOTHING, db_column='id_receta')
    id_farmaco = models.ForeignKey('Farmaco', on_delete=models.CASCADE, db_column='id_farmaco')

    class Meta:
        managed = False
        db_table = 'detalle_farmaco'
        

class Diagnostico(models.Model):
    id_diagnostico = models.BigIntegerField(primary_key=True)
    nombre_diag = models.CharField(max_length=100)
    id_tipo_diag = models.ForeignKey('TipoDiagnostico', models.DO_NOTHING, db_column='id_tipo_diag')

    class Meta:
        managed = False
        db_table = 'diagnostico'

class Especialidad(models.Model):
    id_espec = models.BigIntegerField(primary_key=True)
    nombre_espec = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'especialidad'

class EstadoCivil(models.Model):
    id_estado = models.BigIntegerField(primary_key=True)
    nombre_estado = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'estado_civil'

class Examen(models.Model):
    id_examen = models.BigIntegerField(primary_key=True)
    nombre_examen = models.CharField(max_length=100)
    id_tipo_exam = models.ForeignKey('TipoExamen', models.DO_NOTHING, db_column='id_tipo_exam')

    class Meta:
        managed = False
        db_table = 'examen'

class Farmaco(models.Model):
    id_farmaco = models.BigIntegerField(primary_key=True)
    nombre_farmaco = models.CharField(max_length=100)
    via_administracion = models.CharField(max_length=100)
    contraindicacion = models.CharField(max_length=500, blank=True, null=True)
    id_tipo_farma = models.ForeignKey('TipoFarmaco', models.DO_NOTHING, db_column='id_tipo_farma')

    class Meta:
        managed = False
        db_table = 'farmaco'

class Genero(models.Model):
    id_genero = models.BigIntegerField(primary_key=True)
    nombre_genero = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'genero'

class Licencia(models.Model):
    id_licencia = models.BigIntegerField(primary_key=True)
    fecha_ini_lic = models.DateField()
    fecha_ter_lic = models.DateField()
    descripcion_lic = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'licencia'

class Medico(models.Model):
    run_medico = models.OneToOneField('Usuario', on_delete=models.CASCADE, db_column='run_medico', primary_key=True)
    fecha_ingreso = models.DateField()
    sueldo = models.BigIntegerField()
    regimen_hrs = models.DecimalField(max_digits=2, decimal_places=1)
    id_espec = models.ForeignKey(Especialidad, models.DO_NOTHING, db_column='id_espec')
    id_contrato = models.ForeignKey(Contrato, models.DO_NOTHING, db_column='id_contrato')
    id_agenda = models.ForeignKey(Agenda, models.DO_NOTHING, db_column='id_agenda')

    class Meta:
        managed = False
        db_table = 'medico'

class Nacionalidad(models.Model):
    id_nacionalidad = models.BigIntegerField(primary_key=True)
    nombre_nac = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'nacionalidad'

class Prevision(models.Model):
    id_prevision = models.BigIntegerField(primary_key=True)
    nombre_prevision = models.CharField(max_length=100)
    id_tipo_prev = models.ForeignKey('TipoPrevision', models.DO_NOTHING, db_column='id_tipo_prev')

    class Meta:
        managed = True
        db_table = 'prevision'

class Paciente(models.Model):
    run_paciente = models.OneToOneField('Usuario', on_delete=models.CASCADE, db_column='run_paciente', primary_key=True)
    peso = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    talla = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    enfermedades = models.CharField(max_length=250, blank=True, null=True)
    medicacion_habitual = models.CharField(max_length=250, blank=True, null=True)
    cirugias = models.CharField(max_length=250, blank=True, null=True)
    observaciones = models.CharField(max_length=250, blank=True, null=True)
    id_prevision = models.ForeignKey(Prevision, models.DO_NOTHING, db_column='id_prevision')
    imc = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    @property
    def cal_imc(self):
        if self.peso > 0  and self.talla > 0 :
            imc = round((self.peso)/((self.talla/100)*(self.talla/100)),2)
            return imc
        else:
            return 0


    class Meta:
        managed = True
        db_table = 'paciente'

class PerfilUsuario(models.Model):
    id_perfil = models.BigIntegerField(primary_key=True)
    nombre_perfil = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'perfil_usuario'

class Recepcionista(models.Model):
    run_recepcionista = models.OneToOneField('Usuario', on_delete=models.CASCADE, db_column='run_recepcionista', primary_key=True)
    fecha_ingreso = models.DateField()
    
    sueldo = models.BigIntegerField()
    id_contrato = models.ForeignKey(Contrato, models.DO_NOTHING, db_column='id_contrato')

    class Meta:
        managed = False
        db_table = 'recepcionista'


class Receta(models.Model):
    id_receta = models.BigIntegerField(primary_key=True)
    fecha_receta = models.DateField()
    descripcion_receta = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'receta'

class Region(models.Model):
    id_region = models.BigIntegerField(primary_key=True)
    nombre_region = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'region'

class Reporte(models.Model):
    id_reporte = models.BigIntegerField(primary_key=True)
    documento = models.TextField()

    class Meta:
        managed = False
        db_table = 'reporte'

class ResultadoExamen(models.Model):
    run_paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, db_column='run_paciente', blank=True, null=True)
    archivo = models.TextField()

    class Meta:
        managed = False
        db_table = 'resultado_examen'

class Telefono(models.Model):
    id_telefono = models.BigAutoField(primary_key=True)
    num_telefono = models.BigIntegerField()
    id_tipo_tel = models.ForeignKey('TipoTelefono', models.DO_NOTHING, db_column='id_tipo_tel')

    class Meta:
        managed = False
        db_table = 'telefono'

class TelefonoUsuario(models.Model):
    id_telefono = models.OneToOneField('Telefono', models.DO_NOTHING, db_column='id_telefono', primary_key=True)
    run_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, db_column='run_usuario')

    class Meta:
        managed = False
        db_table = 'telefono_usuario'
        unique_together = (('id_telefono', 'run_usuario'),)


class TipoContrato(models.Model):
    id_tipo_cont = models.BigIntegerField(primary_key=True)
    nombre_tipo_cont = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tipo_contrato'


class TipoDiagnostico(models.Model):
    id_tipo_diag = models.BigIntegerField(primary_key=True)
    tipo_diag = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tipo_diagnostico'


class TipoExamen(models.Model):
    id_tipo_exam = models.BigIntegerField(primary_key=True)
    tipo_exam = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tipo_examen'


class TipoFarmaco(models.Model):
    id_tipo_farma = models.BigIntegerField(primary_key=True)
    tipo_farma = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tipo_farmaco'


class TipoPrevision(models.Model):
    id_tipo_prev = models.BigIntegerField(primary_key=True)
    tipo_prev = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tipo_prevision'


class TipoTelefono(models.Model):
    id_tipo_tel = models.BigIntegerField(primary_key=True)
    tipo_tel = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tipo_telefono'

