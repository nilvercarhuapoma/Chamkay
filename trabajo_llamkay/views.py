from django.shortcuts import render

def index(request):
    return render(request, 'trabajo_llamkay/index.html')

def nosotros (request):
    return render(request,'trabajo_llamkay/nosotros.html')


def medios(request):
    return render(request,'trabajo_llamkay/medios.html')

def contactanos(request):
    return render(request,'trabajo_llamkay/contactanos.html')


def index(request):
    return render(request, 'index.html', {
        'comunidad': [
            {'name': 'Busco carpintero', 'image': 'engineering.jpg'},
            {'name': 'Busco persona con ofimática', 'image': 'informatica.jpg'},
            {'name': 'Busco trabajadores para entrega de agua', 'image': 'agua.jpg'},
            {'name': 'Busco carpintero', 'image': 'engineering.jpg'},
            {'name': 'Busco persona con ofimática', 'image': 'informatica.jpg'},
            {'name': 'Busco trabajadores para entrega de agua', 'image': 'agua.jpg','text': 'Ubicación: Tingo Maria'},
        ],
        'ciudad': [
            {'name': 'Busco persona con ofimática', 'image': 'informatica.jpg'},
        ],
        'distrito': [
            {'name': 'Busco trabajadores para entrega de agua', 'image': 'agua.jpg'},
        ],
        'departamento': [
            {'name': 'Busco personas para sembrar', 'image': 'campo.jpg'},
            {'name': 'Busco persona con ofimática', 'image': 'informatica.jpg'},
            {'name': 'Busco trabajadores para entrega de agua', 'image': 'agua.jpg'},
        ],
    })