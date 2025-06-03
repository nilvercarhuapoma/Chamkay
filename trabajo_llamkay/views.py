from django.shortcuts import render
from django.templatetags.static import static



def nosotros (request):
    return render(request,'trabajo_llamkay/nosotros.html')


def medios(request):
    return render(request,'trabajo_llamkay/medios.html')

def contactanos(request):
    return render(request,'trabajo_llamkay/contactanos.html')


def index(request):
    default_image = static('images/acceso.png')
    profile_picture_url = (
        request.user.profile_picture.url
        if request.user.is_authenticated and hasattr(request.user, 'profile_picture') and request.user.profile_picture
        else default_image
    )

    return render(request, 'index.html', {
        'profile_picture_url': profile_picture_url,
        'comunidad': [
            {'name': 'Busco carpintero', 'image': 'engineering.jpg'},
            {'name': 'Busco persona con ofimática', 'image': 'informatica.jpg'},
            {'name': 'Busco trabajadores para entrega de agua', 'image': 'agua.jpg'},
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