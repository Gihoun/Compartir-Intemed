from django.contrib import admin
from django.urls import path

from .views import administrator, filtro_usuarios, vista_farmaco, filtro_pacientes, edit_paciente, edit_farmaco
from .views import vista_perfil, edit_perfil, edit_colab, vista_atenciones, vista_reportes, vista_newcolab

urlpatterns = [   
    path('panel/',administrator,name="Dash"),
    path('panel/userg',filtro_usuarios,name="userg"),
    path('panel/editar_colaborador/<id>',edit_colab,name="edit_colab"),
    path('panel/atenciones/<id>',vista_atenciones,name="ateng"),
    path('panel/farmaco',vista_farmaco,name="farmag"),
    path('panel/editar_farmaco/<id>',edit_farmaco,name="edit_farma"),
    path('panel/pacientes',filtro_pacientes,name="pac"),
    path('panel/editar_paciente/<id>',edit_paciente,name="edit_pac"),
    path('panel/perfil',vista_perfil,name="perfilg"),
    path('panel/editar_perfil/<id>',edit_perfil,name="edit_perfil"),
    path('panel/reportes',vista_reportes,name="reportg"),
    path('panel/crear_colab',vista_newcolab,name="crear_colab")
]