# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# por cada instancia de hora se generara por defecto una disponibilidad perteneciente a un medico
# o mas bien el medico genera una disponibilidad con horas identificadas dentro de los dias habiles por semana 
from django.db import models
from modulo_admin.models import *


class agenda_hora(models.Model):
    id_hora = models.BigIntegerField(primary_key=True)
    fecha_hora = models.DateTimeField()

class Disponibilidad(models.Model):
    id_disp = models.BigIntegerField(primary_key=True)
    run_medico = models.ForeignKey('modulo_admin.Medico', models.DO_NOTHING, db_column='run_medico')
    id_horaD = models.ForeignKey("agenda_hora", models.DO_NOTHING, db_column='id_hora')

class det_agenda(models.Model):
    idd = models.ForeignKey('Disponibilidad', models.DO_NOTHING, db_column='id_disp')
    run_pac = models.ForeignKey('modulo_admin.Paciente', models.DO_NOTHING, db_column='run_paciente')
    idda = models.BigIntegerField(primary_key=True) # SOLO PARA REGISTRO 