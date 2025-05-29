from django.shortcuts import render
from .forms import TrabajoForm

def crear_trabajo(request):
    datos = None
    if request.method == 'POST':
        form = TrabajoForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data  # datos para mostrar confirmación
            form = TrabajoForm()       # limpiar formulario después de enviar
    else:
        form = TrabajoForm()
    return render(request, 'trabajos/crear_trabajo.html', {'form': form, 'datos': datos})

def index_trabajo(request):
    return render(request, 'trabajos/index_trabajo.html')



def registro_individual(request):
    horas = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    tiempos = ["00", "15", "30", "45"]
    return render(request, 'trabajos/registro_individual.html', {
        'horas': horas,
        'tiempos': tiempos,
    })

    
def registro_empresa(request):
    return render(request, 'trabajos/registro_empresa.html')



def all_trabajos(request):
    trabajos = trabajos.trabajos.objects.all().order_by('-fecha_publicacion')
    return render(request, 'trabajos/all_trabajos.html', {'trabajos': trabajos})