from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('postulante', 'Postulante'),
        ('empleador', 'Empleador'),
        ('empresa', 'Empresa'),
        ('admin', 'Administrador'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='postulante')
    telefono = models.CharField(max_length=20, blank=True)
    idioma_preferido = models.CharField(max_length=10, default='es')


