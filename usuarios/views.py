from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login as django_login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Count, Q, Sum
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse

import os, traceback, json, logging
from datetime import datetime, timedelta
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from usuarios.models import Usuario, Departamento, Provincia, Distrito, Profile, ActividadReciente, Postulacion, Ofertatrabajo
from usuarios.models import Calificacion, UsuarioHabilidad, Comunidad
from trabajos.models import Trabajo

import logging
import traceback
from django.db import IntegrityError
from .forms import RegisterFormStep1, RegisterFormStep2, RegisterFormStep3
from .models import TrabajosRealizados
from django.contrib.auth import login

from django.contrib.auth import get_user_model

User = get_user_model()


# Configurar logging para debug
logger = logging.getLogger(__name__)

@csrf_protect
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return render(request, 'usuarios/login.html', {
                'error_message': "Por favor ingresa email y contraseña."
            })

        try:
            # Buscar al usuario por email
            user_obj = User.objects.filter(email=email, is_active=True).first()
            if not user_obj:
                return render(request, 'usuarios/login.html', {
                    'error_message': "Correo o contraseña incorrecta."
                })

            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                django_login(request, user)
                messages.success(request, f'Bienvenido {user.first_name or user.username}!')
                return redirect('usuarios:dashboard')
            else:
                return render(request, 'usuarios/login.html', {
                    'error_message': "Correo o contraseña incorrecta."
                })
        except Exception as e:
            return render(request, 'usuarios/login.html', {
                'error_message': f"Ocurrió un error. {str(e)}"
            })

    if request.user.is_authenticated:
        return redirect('usuarios:dashboard')
    return render(request, 'usuarios/login.html')


@login_required
def dashboard(request):
    """Vista del dashboard para usuarios autenticados - Index con perfil"""
    
    try:
        usuario_db = Usuario.objects.get(user=request.user)
        profile = Profile.objects.filter(user=request.user).first()
        
        if not profile:
            profile = Profile.objects.create(user=request.user, id_usuario=usuario_db)

        context = {
            'user': request.user,
            'usuario': usuario_db,
            'profile': profile,
            'comunidad': Comunidad.objects.all(),
            'ciudad': Distrito.objects.all(),
            'distrito': Distrito.objects.all(),
            'departamento': Departamento.objects.all(),


        'comunidad': [
            {'name': 'Busco carpintero', 'image': 'engineering.jpg', 'description': 'Experiencia mínima 3 años', 'location': 'Lima'},
            {'name': 'Busco persona con ofimática', 'image': 'informatica.jpg', 'description': 'Conocimiento en Excel avanzado'},
            {'name': 'Busco trabajadores para entrega de agua', 'image': 'agua.jpg', 'text': 'Ubicación: Tingo Maria', 'urgent': True},
            {'name': 'Busco electricista', 'image': 'electrician.jpg', 'description': 'Certificación vigente'},
            {'name': 'Busco pintor profesional', 'image': 'painter.jpg', 'description': 'Para trabajos residenciales'},
            {'name': 'Busco jardinero', 'image': 'gardener.jpg', 'description': 'Experiencia en mantenimiento de áreas verdes'},
        ],
        'ciudad': [
            {'name': 'Busco persona con ofimática', 'image': 'informatica.jpg', 'city': 'Arequipa', 'posted_date': '2025-06-01'},
            {'name': 'Busco cocinero', 'image': 'chef.jpg', 'city': 'Cusco', 'posted_date': '2025-06-05'},
        ],
        'distrito': [
            {'name': 'Busco trabajadores para entrega de agua', 'image': 'agua.jpg', 'district': 'Miraflores', 'shift': 'mañana'},
            {'name': 'Busco personal de limpieza', 'image': 'cleaning.jpg', 'district': 'San Isidro', 'salary': 'S/ 1500 mensual'},
        ],
        'departamento': [
            {'name': 'Busco personas para sembrar', 'image': 'campo.jpg', 'department': 'Junín', 'experience': '2 años'},
            {'name': 'Busco persona con ofimática', 'image': 'informatica.jpg', 'department': 'Lima'},
            {'name': 'Busco trabajadores para entrega de agua', 'image': 'agua.jpg', 'department': 'Loreto', 'availability': 'Inmediata'},
        ],
        'notifications': [
            {'title': 'Nuevo mensaje de Juan', 'time': 'Hace 2 horas', 'read': False},
            {'title': 'Oferta de trabajo aceptada', 'time': 'Ayer', 'read': True},
            {'title': 'Actualización de perfil requerida', 'time': 'Hace 3 días', 'read': False},
        ],
        'messages': [
            {'from': 'Maria', 'snippet': 'Hola, estoy interesada en tu oferta...', 'time': '10 minutos atrás'},
            {'from': 'Pedro', 'snippet': '¿Podrías enviarme más detalles?', 'time': '2 horas atrás'},
        ],
        'stats': {
            'offers_posted': 12,
            'offers_active': 8,
            'messages_unread': 3,
            'notifications_unread': 2,
        },
        'tips': [
            'Actualiza tu perfil para atraer más candidatos.',
            'Responde rápido a los mensajes para mejorar tu reputación.',
            'Publica ofertas claras y detalladas para obtener mejores postulantes.',
        ],
    }

        return render(request, 'usuarios/dashboard.html', context)

    
    except Usuario.DoesNotExist:
        messages.error(request, "No se encontró tu perfil extendido.")
        return redirect('usuarios:login')

    except Exception as e:
        print(f"Error inesperado en vista dashboard: {str(e)}")
        messages.error(request, "Error al cargar el dashboard.")
        return redirect('usuarios:login')

def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('/')  # Redirige a la página principal después del logout



def validar_correo(request):
    email = request.GET.get('email')
    existe = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': existe})

def register(request):
    if request.method == 'POST':
        form = RegisterFormStep1(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            if cd['password1'] != cd['password2']:
                form.add_error('password2', 'Las contraseñas no coinciden.')
                return render(request, 'usuarios/register.html', {'form': form})

            if User.objects.filter(email=cd['email']).exists():
                form.add_error(None, 'Este correo ya está en uso. Intenta con otro.')
                return render(request, 'usuarios/register.html', {'form': form})

            try:
                user = User.objects.create_user(
                    username=f"user{User.objects.count() + 1}",
                    email=cd['email'],
                    first_name=cd['nombre'],
                    last_name=cd['apellido'],
                    password=cd['password1']
                )

                # Guardar datos en sesión para usarlos luego
                request.session['user_id'] = user.id
                request.session['telefono'] = cd['telefono']
                request.session['dni'] = cd['dni']  # si lo incluiste en el formulario

                return redirect('usuarios:register_two')

            except IntegrityError:
                form.add_error(None, 'Hubo un error al crear el usuario. Inténtalo nuevamente.')
                return render(request, 'usuarios/register.html', {'form': form})

    else:# ✅ Aquí está el retorno que faltaba
        form = RegisterFormStep1()
        
    return render(request, 'usuarios/register.html', {'form': form})


def register_two(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('usuarios:register')

    if request.method == 'POST':
        form = RegisterFormStep2(request.POST)
        if form.is_valid():
            # Guardar en sesión, NO en base de datos todavía
            request.session['direccion'] = form.cleaned_data['direccion']
            request.session['departamento_id'] = form.cleaned_data['departamento'].id_departamento
            request.session['provincia_id'] = form.cleaned_data['provincia'].id_provincia
            request.session['distrito_id'] = form.cleaned_data['distrito'].id_distrito

            return redirect('usuarios:register_three')
    else:
        form = RegisterFormStep2()

    return render(request, 'usuarios/register_two.html', {'form': form})

def register_three(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('usuarios:register')

    if request.method == 'POST':
        form = RegisterFormStep3(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.get(id=user_id)

            # Crear Usuario
            usuario, _ = Usuario.objects.get_or_create(
                user=user,
                defaults={
                    'nombres': user.first_name or 'Nombre',
                    'apellidos': user.last_name or 'Apellido',
                    'username': f'user{user.id}',
                    'email': user.email,
                    'telefono': request.session.get('telefono', ''),
                    'clave': '',  # si no lo usas para nada, puedes eliminar el campo del modelo también
                    'dni': request.session.get('dni', '00000000'),
                    'direccion': request.session.get('direccion', ''),
                    'fecha_nacimiento': None,
                    'sexo': '',
                    'tipo_usuario': 'trabajador',
                    'habilitado': True,
                }
            )


            # Crear Profile con todos los datos completos

            profile, _ = Profile.objects.get_or_create(user=user, id_usuario=usuario)
            profile.direccion = request.session.get('direccion', '')
            profile.id_departamento = Departamento.objects.get(id_departamento=request.session.get('departamento_id'))
            profile.id_provincia = Provincia.objects.get(id_provincia=request.session.get('provincia_id'))
            profile.id_distrito = Distrito.objects.get(id_distrito=request.session.get('distrito_id'))
            profile.habilidades = cd['habilidades']
            profile.redes_sociales = {
                'disponibilidad': cd['disponibilidad'],
                'experiencia': cd['experiencia'],
                'tarifa': str(cd['tarifa']) if cd['tarifa'] else '',
            }
            profile.save()

            # Limpiar sesión
            for key in ['user_id', 'dni', 'telefono', 'direccion', 'departamento_id', 'provincia_id', 'distrito_id']:
                request.session.pop(key, None)


            return redirect('usuarios:login')
    else:
        form = RegisterFormStep3()

    return render(request, 'usuarios/register_three.html', {'form': form})


def cargar_provincias(request):
    id_departamento = request.GET.get('id_departamento')
    provincias = Provincia.objects.filter(id_departamento=id_departamento).values('id_provincia', 'nombre')
    return JsonResponse(list(provincias), safe=False)

def cargar_distritos(request):
    id_provincia = request.GET.get('id_provincia')
    distritos = Distrito.objects.filter(id_provincia=id_provincia).values('id_distrito', 'nombre')
    return JsonResponse(list(distritos), safe=False)


@login_required
def perfil(request):
    try:
        usuario_db = Usuario.objects.get(user=request.user)
        profile = Profile.objects.filter(user=request.user).first()
        if not profile:
            profile = Profile.objects.create(user=request.user, id_usuario=usuario_db)

        postulaciones = Postulacion.objects.filter(id_usuario=usuario_db)
        trabajos = Ofertatrabajo.objects.filter(id_oferta__in=postulaciones.values_list('id_oferta', flat=True))

        trabajos_completados = trabajos.filter(estado=True)
        trabajos_activos = trabajos.filter(estado=False)

        calificacion_promedio = Calificacion.objects.filter(
            id_usuario=usuario_db
        ).aggregate(promedio=Avg('calificacion'))['promedio'] or 0

        inicio_mes = timezone.now().replace(day=1)
        ingresos_mes = trabajos_completados.filter(fecha_fin__gte=inicio_mes).aggregate(total=Sum('sueldo'))['total'] or 0

        total_completados = trabajos_completados.count()
        satisfechos = Calificacion.objects.filter(
            id_usuario=usuario_db,
            calificacion__gte=4
        ).count()

        porcentaje_satisfechos = (satisfechos / total_completados * 100) if total_completados else 0

        actividades = ActividadReciente.objects.filter(usuario=usuario_db).order_by('-fecha')[:5]

        redes = profile.redes_sociales or {}
        disponibilidad = redes.get('disponibilidad', '')
        precio_hora = redes.get('precio_hora', '')

        # Habilidades desde tabla intermedia
        habilidades_usuario = UsuarioHabilidad.objects.filter(id_usuario=usuario_db).select_related('id_habilidad')
        nombres_habilidades = [uh.id_habilidad.nombre for uh in habilidades_usuario]

        context = {
            'usuario': usuario_db,
            'profile': profile,
            'bio': profile.bio or '',
            'foto_url': profile.foto_url.url if profile.foto_url else '',
            'disponibilidad': disponibilidad,
            'precio_hora': precio_hora,
            'departamento': profile.id_departamento.nombre if profile.id_departamento else '',
            'provincia': profile.id_provincia.nombre if profile.id_provincia else '',
            'distrito': profile.id_distrito.nombre if profile.id_distrito else '',
            'categorias': profile.categorias,
            'habilidades': nombres_habilidades,
            'estadisticas': {
                'trabajos_realizados': trabajos.count(),
                'trabajos_activos': trabajos_activos.count(),
                'trabajos_completados': total_completados,
                'calificacion': round(calificacion_promedio, 1),
                'porcentaje_satisfechos': round(porcentaje_satisfechos),
                'ingresos_mes': ingresos_mes,
            },
            'trabajos_recientes': trabajos.order_by('-fecha_fin')[:3],
            'actividades': actividades,
        }

        return render(request, 'usuarios/perfil.html', context)

    except Usuario.DoesNotExist:
        messages.error(request, "No se encontró tu perfil extendido.")
        return redirect('usuarios:login')

    except Exception as e:
        print(f"Error inesperado en vista perfil: {str(e)}")
        print(traceback.format_exc())
        messages.error(request, "Error al cargar el perfil.")
        return redirect('usuarios:dashboard')


   
@login_required
@require_POST
def actualizar_perfil(request):
    usuario_db = Usuario.objects.get(user=request.user)
    profile, _ = Profile.objects.get_or_create(user=request.user, defaults={'id_usuario': usuario_db})

    usuario_db.nombres = request.POST.get('nombres', '')
    usuario_db.apellidos = request.POST.get('apellidos', '')
    usuario_db.telefono = request.POST.get('telefono', '')
    usuario_db.save()

    profile.bio = request.POST.get('descripcion', '')
    profile.id_departamento = Departamento.objects.get(id_departamento=request.POST.get('departamento')) if request.POST.get('departamento') else None
    profile.id_provincia = Provincia.objects.get(id_provincia=request.POST.get('provincia')) if request.POST.get('provincia') else None
    profile.id_distrito = Distrito.objects.get(id_distrito=request.POST.get('distrito')) if request.POST.get('distrito') else None

    redes = profile.redes_sociales or {}
    redes['disponibilidad'] = request.POST.get('disponibilidad', '')
    redes['precio_hora'] = request.POST.get('precio_hora', '')
    profile.redes_sociales = redes

    if 'foto' in request.FILES:
        profile.foto_url = request.FILES['foto']
    profile.save()

    # Guardar habilidades
    ah_ids = request.POST.getlist('habilidades')
    profile.categorias = ','.join(ah_ids)
    profile.save()
    # Opcional: borrar/crear UsuarioHabilidad según ah_ids

    ActividadReciente.objects.create(usuario=usuario_db, descripcion='Perfil modificado', fecha=timezone.now())
    return JsonResponse({'success': True})

@login_required
def actualizar_servicios(request):
    """Actualizar servicios del usuario"""
    if request.method == 'POST':
        try:
            usuario_db = Usuario.objects.get(user=request.user)
            profile = Profile.objects.get(user=request.user)
            
            servicios = request.POST.getlist('servicios[]')
            profile.habilidades = ','.join(servicios)  # Guardar como string separado por comas
            profile.save()
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
def historial_trabajos(request):
    """Obtener historial de trabajos del usuario"""
    try:
        usuario_db = Usuario.objects.get(user=request.user)
        trabajos = []  # Inicializar como lista vacía si no hay modelo Trabajo
        
        try:
            trabajos = Trabajo.objects.filter(trabajador=usuario_db).order_by('-fecha_creacion')
        except:
            # Si no existe el modelo Trabajo, usar datos dummy o vacío
            pass
        
        trabajos_data = []
        for trabajo in trabajos:
            trabajos_data.append({
                'id': trabajo.id_trabajo,
                'titulo': trabajo.titulo,
                'descripcion': trabajo.descripcion,
                'cliente': f"{trabajo.cliente.nombres} {trabajo.cliente.apellidos}",
                'estado': trabajo.estado,
                'fecha_creacion': trabajo.fecha_creacion.strftime('%d %b %Y'),
                'precio': float(trabajo.precio),
                'calificacion': trabajo.calificacion,
                'ubicacion': trabajo.ubicacion,
                'icono': get_icono_servicio(trabajo.tipo_servicio)
            })
        
        return JsonResponse({'trabajos': trabajos_data})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def get_icono_servicio(tipo_servicio):
    """Obtener icono según el tipo de servicio"""
    iconos = {
        'limpieza': '🧹',
        'cuidado_ninos': '👶',
        'cocina': '🍳',
        'jardineria': '🌱',
        'electricidad': '⚡',
        'plomeria': '🔧',
        'carpinteria': '🔨',
        'pintura': '🎨',
    }
    return iconos.get(tipo_servicio, '🏠')

@login_required
def obtener_estadisticas(request):
    """API para obtener estadísticas del usuario"""
    try:
        usuario_db = Usuario.objects.get(user=request.user)
        trabajos = []
        
        try:
            trabajos = Trabajo.objects.filter(trabajador=usuario_db)
        except:
            pass
        
        # Estadísticas por mes (últimos 6 meses)
        estadisticas_mes = []
        for i in range(6):
            fecha = datetime.now() - timedelta(days=30*i)
            trabajos_mes = 0
            if trabajos:
                trabajos_mes = trabajos.filter(
                    fecha_creacion__year=fecha.year,
                    fecha_creacion__month=fecha.month
                ).count()
            estadisticas_mes.append({
                'mes': fecha.strftime('%B'),
                'trabajos': trabajos_mes
            })
        
        ingresos_total = 0
        if trabajos:
            ingresos_total = trabajos.filter(estado='completado').aggregate(
                total=Sum('precio')
            )['total'] or 0
        
        return JsonResponse({
            'estadisticas_mes': estadisticas_mes[::-1],  # Invertir para orden cronológico
            'total_trabajos': len(trabajos),
            'ingresos_total': ingresos_total
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required  
def configuracion(request):
    """Vista de configuración - versión mejorada"""
    try:
        print(f"=== DEBUG CONFIGURACION ===")
        print(f"Usuario: {request.user}")
        
        context = {
            'user': request.user,
            'title': 'Configuración y Privacidad',
        }
        
        # Crear un template simple si no existe
        try:
            return render(request, 'usuarios/configuracion.html', context)
        except:
            # Template de respaldo
            return render(request, 'usuarios/simple_page.html', {
                **context,
                'page_title': 'Configuración y Privacidad',
                'page_content': 'Página de configuración en desarrollo.'
            })
        
    except Exception as e:
        print(f"ERROR EN CONFIGURACION: {str(e)}")
        messages.error(request, f"Error al cargar configuración: {str(e)}")
        return redirect('usuarios:dashboard')

@login_required
def ayuda(request):
    """Vista de ayuda - versión mejorada"""
    try:
        context = {
            'user': request.user,
            'title': 'Ayuda y Soporte Técnico',
        }
        try:
            return render(request, 'usuarios/ayuda.html', context)
        except:
            return render(request, 'usuarios/simple_page.html', {
                **context,
                'page_title': 'Ayuda y Soporte Técnico',
                'page_content': 'Página de ayuda en desarrollo.'
            })
    except Exception as e:
        print(f"ERROR EN AYUDA: {str(e)}")
        return redirect('usuarios:dashboard')

@login_required
def accesibilidad(request):
    """Vista de accesibilidad - versión mejorada"""
    try:
        context = {
            'user': request.user,
            'title': 'Pantalla y Accesibilidad',
        }
        try:
            return render(request, 'usuarios/accesibilidad.html', context)
        except:
            return render(request, 'usuarios/simple_page.html', {
                **context,
                'page_title': 'Pantalla y Accesibilidad',
                'page_content': 'Página de accesibilidad en desarrollo.'
            })
    except Exception as e:
        print(f"ERROR EN ACCESIBILIDAD: {str(e)}")
        return redirect('usuarios:dashboard')
    
@login_required
def comentarios(request):
    """Vista de comentarios - versión mejorada"""
    try:
        context = {
            'user': request.user,
            'title': 'Enviar Comentarios',
        }
        try:
            return render(request, 'usuarios/comentarios.html', context)
        except:
            return render(request, 'usuarios/simple_page.html', {
                **context,
                'page_title': 'Enviar Comentarios',
                'page_content': 'Página de comentarios en desarrollo.'
            })
    except Exception as e:
        print(f"ERROR EN COMENTARIOS: {str(e)}")
        return redirect('usuarios:dashboard')
    