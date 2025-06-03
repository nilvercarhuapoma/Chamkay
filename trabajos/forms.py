from django import forms
from .models import OfertaUsuario, OfertaEmpresa

class OfertaUsuarioForm(forms.ModelForm):
    class Meta:
        model = OfertaUsuario
        exclude = ['empleador', 'estado', 'fecha_registro']
        widgets = {
            'horas_limite': forms.TimeInput(format='%H:%M:%S', attrs={'type': 'time'}),
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
        }

class OfertaEmpresaForm(forms.ModelForm):
    class Meta:
        model = OfertaEmpresa
        fields = [
            'titulo_puesto',
            'rango_salarial',
            'experiencia_requerida',
            'modalidad_trabajo',
            'descripcion_puesto',
            'requisitos_calificaciones',
            'beneficios_compensaciones',
            'numero_postulantes',
            'foto',
            'fecha_limite',
            'id_departamento',
            'id_provincia',
            'id_distrito',
            'id_comunidad',
            'direccion_detalle',
        ]
        widgets = {
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
            'descripcion_puesto': forms.Textarea(attrs={'rows': 3}),
            'requisitos_calificaciones': forms.Textarea(attrs={'rows': 3}),
            'beneficios_compensaciones': forms.Textarea(attrs={'rows': 3}),
            'direccion_detalle': forms.Textarea(attrs={'rows': 2}),
        }