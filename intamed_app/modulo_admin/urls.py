from django.contrib import admin
from django.urls import path
from .views import administrator, filtro_usuarios, vista_farmaco, filtro_pacientes, edit_paciente, edit_farmaco

urlpatterns = [   
    path('panel/',administrator,name="Dash"),
    path('panel/userg',filtro_usuarios,name="userg"),
    path('panel/farmaco',vista_farmaco,name="farmag"),
    path('panel/pacientes',filtro_pacientes,name="pac"),
    path('panel/editar_paciente/<id>',edit_paciente,name="edit_pac"),
    path('panel/editar_farmaco/<id>',edit_farmaco,name="edit_farma")

]