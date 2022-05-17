from django.contrib import admin
from .models import Usuario, Atencion, Diagnostico, Paciente
# Register your models here.

admin.site.register(Usuario)
admin.site.register(Atencion)
admin.site.register(Diagnostico)
admin.site.register(Paciente)
