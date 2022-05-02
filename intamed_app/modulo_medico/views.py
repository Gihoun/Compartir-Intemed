import re
from django.shortcuts import render

# Create your views here.

def inicio(request):
    return render(request,"base_medico.html")

def micuenta(request):
    return render(request,"mi-cuenta.html")

def nuestraclinica(request):
    return render(request,"nuestra-clinica.html")

def funcionarios(request):
    return render(request,"funcionarios.html")    