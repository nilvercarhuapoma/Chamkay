from django import forms

class TrabajoForm(forms.Form):
    titulo = forms.CharField(
        max_length=200,
        label="Título",
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese el título'})
    )
    descripcion = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(attrs={'placeholder': 'Descripción del trabajo'})
    )
    
    
    fecha_limite = forms.DateField(
        label="Fecha límite",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    pago = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        label="Pago",
        widget=forms.NumberInput(attrs={'placeholder': 'Monto a pagar(opcional)'})
    )
    herramientas = forms.CharField(
        label="Herramientas",
        widget=forms.Textarea(attrs={'placeholder': 'Herramientas separadas por comas'})
    )
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('vencida', 'Vencida'),
        ('completada', 'Completada'),
    ]
    estado = forms.ChoiceField(
        choices=ESTADO_CHOICES,
        label="Estado"
    )
