from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from trabajos.models import OfertaUsuario
from trabajos.forms import OfertaUsuarioForm 
from trabajos.models import OfertaEmpresa
from trabajos.forms import OfertaEmpresaForm 
from datetime import time
from django.http import JsonResponse
from usuarios.models import Departamento, Provincia, Distrito, Comunidad
from itertools import chain
from django.utils.timezone import now



@login_required
def registro_individual(request):
    if request.user.tipo_usuario not in ['ofrecer-trabajo', 'ambos']:
        raise PermissionDenied("No tienes permiso para registrar una oferta como usuario individual.")

    if request.method == 'POST':
        form = OfertaUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.empleador = request.user

            # Procesar la hora ingresada manualmente
            try:
                hora = int(request.POST.get('hora', 0))
                minuto = int(request.POST.get('minuto', 0))
                segundo = int(request.POST.get('segundo', 0))
                ampm = request.POST.get('ampm', 'AM').upper()

                if ampm == 'PM' and hora != 12:
                    hora += 12
                if ampm == 'AM' and hora == 12:
                    hora = 0

                oferta.horas_limite = time(hora, minuto, segundo)
            except Exception:
                form.add_error(None, "Error al procesar la hora límite.")
                return render(request, 'trabajos/registro_individual.html', {
                    'form': form,
                    'horas': ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
                    'tiempos': ["00", "15", "30", "45"],
                })

            oferta.save()
            return redirect('trabajos:all_trabajos')  # Asegúrate de tener esta URL configurada

    else:
        form = OfertaUsuarioForm()

    horas = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    tiempos = ["00", "15", "30", "45"]
    return render(request, 'trabajos/registro_individual.html', {
        'form': form,
        'horas': horas,
        'tiempos': tiempos,
    })

@login_required
def registro_empresa(request):
    if request.user.tipo_usuario != 'empresa':
        raise PermissionDenied("No tienes permiso para registrar una oferta como empresa.")

    if request.method == 'POST':
        form = OfertaEmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.empleador = request.user
            oferta.save()
            return redirect('trabajos:all_trabajos')  # Redirige a la lista general de trabajos
    else:
        form = OfertaEmpresaForm()

    departamentos = Departamento.objects.all()  # O el queryset que corresponda

    return render(request, 'trabajos/registro_empresa.html', {
        'form': form,
        'departamentos': departamentos,  # Aquí pasas departamentos al template
    })

def index_trabajo(request):
    return render(request, 'trabajos/index_trabajo.html')


def all_trabajos(request):
    ofertas_usuario = OfertaUsuario.objects.filter(estado='activa')
    ofertas_empresa = OfertaEmpresa.objects.filter(estado='activa')

    trabajos = []

    for o in ofertas_usuario:
        trabajos.append({
            'tipo': 'usuario',
            'titulo': o.titulo,
            'descripcion': o.descripcion,
            'herramientas': o.herramientas,
            'pago': o.pago,
            'foto': o.foto,
            'fecha_registro': o.fecha_registro,
            'fecha_limite': o.fecha_limite,
            'horas_limite': o.horas_limite,
            'rango_salarial': None,
            'experiencia_requerida': None,
            'modalidad_trabajo': None,
            'requisitos_calificaciones': None,
            'beneficios_compensaciones': None,
            'numero_postulantes': None,
            'id_departamento': o.id_departamento,
            'id_provincia': o.id_provincia,
            'id_distrito': o.id_distrito,
            'id_comunidad': o.id_comunidad,
        })

    for o in ofertas_empresa:
        trabajos.append({
            'tipo': 'empresa',
            'titulo': o.titulo_puesto,
            'descripcion': o.descripcion_puesto,
            'herramientas': None,
            'pago': None,
            'foto': o.foto,
            'fecha_registro': o.fecha_registro,
            'fecha_limite': o.fecha_limite,
            'horas_limite': None,
            'rango_salarial': o.rango_salarial,
            'experiencia_requerida': o.experiencia_requerida,
            'modalidad_trabajo': o.modalidad_trabajo,
            'requisitos_calificaciones': o.requisitos_calificaciones,
            'beneficios_compensaciones': o.beneficios_compensaciones,
            'numero_postulantes': o.numero_postulantes,
            'id_departamento': o.id_departamento,
            'id_provincia': o.id_provincia,
            'id_distrito': o.id_distrito,
            'id_comunidad': o.id_comunidad,
        })

    return render(request, "trabajos/all_trabajos.html", {'trabajos': trabajos})

    
    
    
    
def ajax_provincias(request):
    departamento_id = request.GET.get('id_departamento')
    provincias = []
    if departamento_id:
        provincias = list(Provincia.objects.filter(id_departamento=departamento_id).values('id_provincia', 'nombre'))
    return JsonResponse({'provincias': provincias})

def ajax_distritos(request):
    provincia_id = request.GET.get('id_provincia')
    distritos = []
    if provincia_id:
        distritos = list(Distrito.objects.filter(id_provincia=provincia_id).values('id_distrito', 'nombre'))
    return JsonResponse({'distritos': distritos})

def ajax_comunidades(request):
    distrito_id = request.GET.get('id_distrito')
    comunidades = []
    if distrito_id:
        comunidades = list(Comunidad.objects.filter(id_distrito=distrito_id).values('id_comunidad', 'nombre'))
    return JsonResponse({'comunidades': comunidades})














