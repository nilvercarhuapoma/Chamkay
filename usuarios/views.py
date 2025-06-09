from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Usuario, Departamento, Provincia, Distrito
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

def login(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        clave = request.POST.get('clave')

        user = authenticate(request, email=email, clave=clave)
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
            error_message = "Este correo ya está registrado."
            return render(request, 'usuarios/register.html', {'error_message': error_message})

        if clave != clave_confirm:
            error_message = "Las contraseñas no coinciden."
            return render(request, 'usuarios/register.html', {'error_message': error_message})

        # Guardamos temporalmente los datos en sesión
        request.session['temp_register'] = {
            'nombre': nombre,
            'email': email,
            'clave': clave,
            'telefono': telefono
        }

        return redirect('usuarios:register_two')

    return render(request, 'usuarios/register.html')



def register_two(request):
    departamentos = Departamento.objects.all()

    if request.method == 'POST':
        departamento_id = request.POST.get('departamento')
        provincia_id = request.POST.get('provincia')
        distrito_id = request.POST.get('distrito')

        temp_data = request.session.get('temp_register')

        if not temp_data:
            return redirect('usuarios:register')  # Si se pierde la sesión, vuelve al inicio

        # Verificamos que la ubicación sea válida
        try:
            departamento = Departamento.objects.get(id_departamento=departamento_id)
            provincia = Provincia.objects.get(id_provincia=provincia_id)
            distrito = Distrito.objects.get(id_distrito=distrito_id)

        except Exception as e:
            return render(request, 'usuarios/register_two.html', {
                'departamentos': departamentos,
                'error_message': 'Ubicación inválida'
            })
        
        usuario = Usuario(
            nombres=temp_data['nombre'],
            email=temp_data['email'],
            clave=make_password(temp_data['clave']),
            telefono=temp_data['telefono'],
            id_departamento=departamento,
            id_provincia=provincia,
            id_distrito=distrito
        )
        usuario.save()

        del request.session['temp_register']

        return render(request, 'usuarios/registro_completado.html', {'usuario': usuario})

    return render(request, 'usuarios/register_two.html', {
        'departamentos': departamentos,
    })



def cargar_provincias(request):
    departamento_id = request.GET.get('departamento_id')
    provincias = Provincia.objects.filter(id_departamento=departamento_id).values('id_provincia', 'nombre')
    return JsonResponse(list(provincias), safe=False)

def cargar_distritos(request):
    provincia_id = request.GET.get('provincia_id')
    distritos = Distrito.objects.filter(id_provincia=provincia_id).values('id_distrito', 'nombre')
    return JsonResponse(list(distritos), safe=False)

