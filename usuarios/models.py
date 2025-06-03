from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UsuarioManager
from django.conf import settings

class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    
    class Meta:
        managed = True
        db_table = 'departamento'
        

class Provincia(models.Model):
    id_provincia = models.AutoField(primary_key=True)
    nombre = models.CharField(blank=True, null=True)
    id_departamento = models.ForeignKey(Departamento, on_delete=models.DO_NOTHING, db_column='id_departamento')
    class Meta:
        managed =True
        db_table = 'provincia'

  
class Distrito(models.Model):
    id_distrito = models.IntegerField(primary_key=True)
    nombre = models.CharField(blank=True, null=True)
    id_provincia = models.ForeignKey(Provincia, on_delete=models.DO_NOTHING, db_column='id_provincia')

    class Meta:
        managed =True
        db_table = 'distrito'


class Comunidad(models.Model):
    id_comunidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    id_distrito = models.ForeignKey(Distrito, on_delete=models.DO_NOTHING, db_column='id_distrito')

    class Meta:
        db_table = 'comunidad'
        managed = True

class Calle(models.Model):
    id_calle = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    # Relaciones directas a todos los niveles
    id_departamento = models.ForeignKey('Departamento', on_delete=models.DO_NOTHING, db_column='id_departamento')
    id_ciudad = models.ForeignKey('Provincia', on_delete=models.DO_NOTHING, db_column='id_provincia')
    id_distrito = models.ForeignKey('Distrito', on_delete=models.DO_NOTHING, db_column='id_distrito')
    id_comunidad = models.ForeignKey('Comunidad', on_delete=models.DO_NOTHING, db_column='id_comunidad')

    class Meta:
        managed = True
        db_table = 'calle'
        
        

class Usuario(AbstractBaseUser, PermissionsMixin):
    ROL_CHOICES = [
        ('buscar-trabajo', 'Buscar trabajo'),
        ('ofrecer-trabajo', 'Ofrecer trabajo'),
        ('ambos', 'Buscar y ofrecer trabajo'),
        ('empresa', 'Como empresa'),  
    ]

    id_usuario = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=150, blank=True, null=True)
    apellidos = models.CharField(max_length=150, blank=True, null=True)
    dni = models.CharField(max_length=20, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    
    fecha_nacimiento = models.DateField(blank=True, null=True)
    sexo = models.CharField(max_length=10, blank=True, null=True)
    tipo_usuario = models.CharField(max_length=30, choices=ROL_CHOICES, blank=True, null=True)
    habilitado = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    id_provincia = models.ForeignKey(Provincia, models.DO_NOTHING, db_column='id_provincia', blank=True, null=True)
    id_distrito = models.ForeignKey(Distrito, models.DO_NOTHING, db_column='id_distrito', blank=True, null=True)
    id_calle = models.ForeignKey(Calle, models.DO_NOTHING, db_column='id_calle', blank=True, null=True)
    id_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='id_departamento', blank=True, null=True)
    id_comunidad = models.ForeignKey(Comunidad, models.DO_NOTHING, db_column='id_comunidad', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UsuarioManager()

    class Meta:
        db_table = 'usuario'


class Empresa(models.Model):
    id_empresa = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=255)
    ruc = models.CharField(max_length=20, unique=True)
    email_empresa = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    clave = models.CharField(max_length=128)
    profile_picture = models.ImageField(upload_to='profiles_empresas/', blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    habilitado = models.BooleanField(default=True)

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='empresa')  # ✅ relación

    class Meta:
        managed = True
        db_table = 'empresa'

    def __str__(self):
        return self.nombre_empresa

