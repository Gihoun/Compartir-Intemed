from django.contrib import admin
from .models import Usuario, Atencion, Diagnostico, Paciente
from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
# Register your models here.

admin.site.register(Usuario)
admin.site.register(Atencion)
admin.site.register(Diagnostico)
admin.site.register(Paciente)


