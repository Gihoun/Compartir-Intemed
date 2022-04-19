from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required,permission_required
### Vista de Prueba de  Response
def inicio_medico(request):
    
    return render(request,"base_medico.html")
