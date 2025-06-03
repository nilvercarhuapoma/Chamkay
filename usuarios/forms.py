# usuarios/forms.py
from django import forms
from .models import Usuario  # tu modelo de perfil

class FotoPerfilForm(forms.ModelForm):
    class Meta:
        model =Usuario
        fields = ['profile_picture']  # asegúrate de tener este campo en el modelo
