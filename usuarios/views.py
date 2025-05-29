from django.shortcuts import render

from .models import Usuario, Departamento, Provincia, Distrito
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate
# Create your views here.
def login(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        clave = request.POST.get('clave')

        user = authenticate(request, username=email, password=clave)
        if user is not None:
            return render(request, 'trabajo_llamkay/base/base.html', {'user': user})
        else:
            error_message = "Invalid email or password."
            return render(request, 'usuarios/login.html', {'error_message': error_message})
    
    return render(request,'usuarios/login.html')

def register(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        clave = request.POST.get('clave')
        telefono = request.POST.get('telefono')
        clave_confirm = request.POST.get('clave_confirm')

        if Usuario.objects.filter(email=email).exists():
            error_message = "Email already exists."
            return render(request, 'usuarios/register.html', {'error_message': error_message})
        
        if clave != clave_confirm:
            error_message = 'This Password is not match'
            return render(request, 'usuarios/register.html', {'error message': error_message})

        usuario = Usuario(
            nombres=nombre,
            email=email,
            clave=make_password(clave),
            telefono=telefono
        )
        usuario.save()
        return render(request, 'usuarios/register_two.html')
    
    return render(request, 'usuarios/register.html')




def register_two(request):
    departamentos = Departamento.objects.all()

    if request.method == 'POST':
        departamento_id = Departamento.POST.get('departamento')
        try:
            departamento = Departamento.objects.get(id_departamento=departamento_id)
        except Departamento.DoesNotExist:
            return render(request, 'usuarios/register_two.html',
                {'departamentos': departamentos},
                {'error message': 'No existe'}
            )
        
        provincia = request.POST.get('provincia')
        distrito = request.POST.get('distrito')

    
        #provincia = Provincia(nombre=provincia, departamento=departamento)

        #provincia_id = Provincia.POST.get('provincia')
        

    return render(request, 'usuarios/register_two.html', {'departamentos': departamentos})

