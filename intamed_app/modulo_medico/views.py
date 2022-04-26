import re
from django.shortcuts import render

# Create your views here.

def inicio(request):
    return render(request,"base_medico.html")


def administrator(request):
    
    return render(request,"administrator.html")