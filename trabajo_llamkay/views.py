from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def index(request):
    return render(request, 'trabajo_llamkay/index.html')

def nosotros (request):
    return render(request,'trabajo_llamkay/nosotros.html')


def medios(request):
    return render(request,'trabajo_llamkay/medios.html')

def contactanos(request):
    return render(request,'trabajo_llamkay/contactanos.html')