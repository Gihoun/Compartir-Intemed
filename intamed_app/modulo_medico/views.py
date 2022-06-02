from django.shortcuts import render

# Create your views here.

def inicio(request):
    return render(request,"base_medico.html")

  

def prueba(request):
    return render(request,"contenido_medico.html")