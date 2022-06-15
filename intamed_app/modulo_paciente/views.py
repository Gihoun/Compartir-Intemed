from django.shortcuts import render
from modulo_admin.models import *
# Create your views here.


def inicio(request):

    return render(request,"base_paciente.html")