from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout
from .models import Usuario, Departamento,Provincia, Distrito
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login as auth_login
from .forms import FotoPerfilForm 
from .models import Empresa

# Create your views here.

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            if remember:
                request.session.set_expiry(1209600)  # 2 semanas
            else:
                request.session.set_expiry(0)  # Expira al cerrar navegador
            return redirect('trabajo_llamkay:home')
        else:
            error_message = "Correo o contraseña incorrectos."
            return render(request, 'usuarios/login.html', {'error_message': error_message})

    return render(request, 'usuarios/login.html')

@login_required
def actualizar_foto(request):
    if request.method == 'POST':
        form = FotoPerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('usuarios:perfil')  # asegúrate que esta URL existe
    else:
        form = FotoPerfilForm(instance=request.user)
    
    return render(request, 'usuarios/actualizar_foto.html', {'form': form})

@login_required
def actualizar_foto_empresa(request):
    empresa = getattr(request.user, 'empresa', None)

    if request.method == 'POST' and empresa:
        nueva_foto = request.FILES.get('profile_picture', None)

        if nueva_foto:
            empresa.profile_picture = nueva_foto
        # Si no se sube nueva imagen y la actual es None, aseguramos que no quede vacía
        elif not empresa.profile_picture:
            empresa.profile_picture = None  # Esto mantiene vacío (la plantilla mostrará la foto por defecto)

        empresa.save()

    return redirect('usuarios:perfil_empresa')







def register(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        clave = request.POST.get('clave')
        clave_confirm = request.POST.get('clave_confirm')
        telefono = request.POST.get('telefono')

        # Recuperar tipo de usuario desde la sesión (si proviene de un paso previo)
        tipo_registro = request.session.get('tipo_registro')

        # Validaciones básicas
        if not email:
            return render(request, 'usuarios/register.html', {'error_message': "El campo email es obligatorio."})

        if Usuario.objects.filter(email=email).exists():
            return render(request, 'usuarios/register.html', {'error_message': "Este email ya está registrado."})

        if clave != clave_confirm:
            return render(request, 'usuarios/register.html', {'error_message': 'Las contraseñas no coinciden.'})

        # Mapear tipo de usuario
        mapa_roles = {
            'buscar': 'buscar-trabajo',
            'ofrecer': 'ofrecer-trabajo',
            'ambos': 'ambos',
            'empresa': 'empresa',
        }
        tipo_usuario = mapa_roles.get(tipo_registro)

        # Crear usuario (incompleto por ahora, se complementa en paso 2)
        usuario = Usuario.objects.create_user(
             email=email,
              password=clave,
              nombres=nombre,
              telefono=telefono,
             tipo_usuario=tipo_usuario
            )

        # Guardar ID del usuario en sesión para continuar en el siguiente paso
        request.session['usuario_id'] = usuario.id_usuario

        # Redirigir a paso 2
        return redirect('usuarios:register_two')

    return render(request, 'usuarios/register.html')



def register_two(request):
    departamentos = Departamento.objects.all()
    provincias = Provincia.objects.all()

    if request.method == 'POST':
        direccion = request.POST.get('direccion')
        departamento_id = request.POST.get('departamento')
        provincia_id = request.POST.get('provincia')

        usuario_id = request.session.get('usuario_id')

        if not usuario_id:
            return redirect('usuarios:register')  # Seguridad: si se salta paso 1

        try:
            usuario = Usuario.objects.get(id_usuario=usuario_id)

            usuario.direccion = direccion

            if departamento_id:
                departamento_obj = Departamento.objects.filter(id_ciudad=departamento_id).first()
                usuario.id_departamento = departamento_obj

            if provincia_id:
                provincia_obj = Provincia.objects.filter(id_provincia=provincia_id).first()
                usuario.id_provincia = provincia_obj

            usuario.save()

            # Limpiar la sesión (fin del registro)
            if 'usuario_id' in request.session:
                del request.session['usuario_id']

            return redirect('usuarios:login')

        except Usuario.DoesNotExist:
            return render(request, 'usuarios/register_two.html', {
                'error_message': 'Usuario no encontrado.',
                'departamentos': departamentos,
                'provincias': provincias,
            })

    return render(request, 'usuarios/register_two.html', {
        'departamentos': departamentos,
        'provincias': provincias,
    })

def seleccionar_registro(request):
    if request.method == 'POST':
        opcion = request.POST.get('tipo_registro')

        # Guardar en sesión
        request.session['tipo_registro'] = opcion

        if opcion in ['buscar', 'ofrecer', 'ambos']:
            return redirect('usuarios:register')
        elif opcion == 'empresa':
            return redirect('usuarios:registro_empleador')
            
    return render(request, 'usuarios/seleccionar_registro.html')





def registro_empleador(request):
    if request.method == 'POST':
        nombre_empresa = request.POST.get('nombre_empresa')
        ruc = request.POST.get('ruc')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        confirmar_contrasena = request.POST.get('confirmar_contrasena')

        if contrasena != confirmar_contrasena:
            return render(request, 'usuarios/registro_empleador.html', {
                'error_message': 'Las contraseñas no coinciden.'
            })

        if Empresa.objects.filter(ruc=ruc).exists():
            return render(request, 'usuarios/registro_empleador.html', {
                'error_message': 'El RUC ya está registrado.'
            })

        if Empresa.objects.filter(email_empresa=correo).exists():
            return render(request, 'usuarios/registro_empleador.html', {
                'error_message': 'El correo ya está registrado.'
            })

        if Usuario.objects.filter(email=correo).exists():
            return render(request, 'usuarios/registro_empleador.html', {
                'error_message': 'Ya existe un usuario con este correo.'
            })

        # 1. Crear usuario con rol "empresa"
        usuario = Usuario.objects.create_user(
            email=correo,
            password=contrasena,
            tipo_usuario='empresa'
        )

        # 2. Crear Empresa vinculada a ese usuario
        empresa = Empresa.objects.create(
            nombre_empresa=nombre_empresa,
            ruc=ruc,
            direccion=direccion,
            telefono=telefono,
            email_empresa=correo,
            clave=contrasena,  # Lo ideal es no guardar la contraseña aquí, o hashearla
            usuario=usuario
        )

        # 3. No iniciar sesión automáticamente, solo redirigir a login
        # auth_login(request, usuario)  <-- línea eliminada/commentada

        return redirect('usuarios:login')  # Redirige a la página de login

    return render(request, 'usuarios/registro_empleador.html')




@login_required
def profile_view(request):
    return render(request, 'usuarios/profile.html')



@login_required
def perfil_empresa(request):
    try:
        empresa = request.user.empresa  # relación OneToOne
    except Empresa.DoesNotExist:
        empresa = None

    return render(request, 'usuarios/perfil_empresa.html', {'empresa': empresa})

def logout_view(request):
    logout(request)
    return redirect('trabajo_llamkay:home') 








