# usuarios/forms.py
from django import forms
from usuarios.models import Usuario, Profile 
from usuarios.models import Departamento, Provincia, Distrito

class RegisterFormStep1(forms.Form):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    email = forms.EmailField()
    telefono = forms.CharField(max_length=20)
    dni = forms.CharField(max_length=8)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


class RegisterFormStep2(forms.Form):
    direccion = forms.CharField(max_length=255, required=True)

    # Solo se usa el queryset en el servidor (para validación y guardado), no para mostrar opciones en HTML
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(), required=True, empty_label=None
    )
    provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.all(), required=True, empty_label=None
    )
    distrito = forms.ModelChoiceField(
        queryset=Distrito.objects.all(), required=True, empty_label=None
    )



class RegisterFormStep3(forms.Form):
    habilidades = forms.CharField(
        widget=forms.Textarea(attrs={'id': 'habilidades', 'required': True}),
        label="Habilidades y oficios *"
    )
    experiencia_choices = [
        ('', 'Selecciona tu año de experiencia'),
        ('1', '1 año'),
        ('1-3', '1 - 3 años'),
        ('3-5', '3 - 5 años'),
        ('5+', '5 + años'),
    ]
    experiencia = forms.ChoiceField(
        choices=experiencia_choices,
        required=False,
        label="Experiencia"
    )
    disponibilidad_choices = [
        ('', 'Selecciona tu disponibilidad'),
        ('mañanas', 'Solo mañanas'),
        ('tardes', 'Solo tardes'),
        ('todo_dia', 'Todo el día'),
    ]
    disponibilidad = forms.ChoiceField(
        choices=disponibilidad_choices,
        required=True,
        label="Disponibilidad *"
    )
    tarifa = forms.DecimalField(
        required=False,
        min_value=0,
        label="Tarifa por hora (opcional)",
        initial=16,
        widget=forms.NumberInput(attrs={'id': 'tarifa'})
    )

email = forms.EmailField(
    label="Correo electrónico",
    widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com'}),
)
