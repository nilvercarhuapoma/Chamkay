#hagan un python manage.py makemigrations usuarios
#luego: python manage.py migrate

from django.db import models
from django.contrib.auth.models import User

class ActividadReciente(models.Model):
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'actividad_reciente'


class Avisos(models.Model):
    id_aviso = models.IntegerField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    mensaje = models.CharField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'avisos'


class Calificacion(models.Model):
    id_calificacion = models.IntegerField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    id_empleador = models.ForeignKey('Empleador', models.DO_NOTHING, db_column='id_empleador', blank=True, null=True)
    calificacion = models.IntegerField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'calificacion'


class Categoriatrabajo(models.Model):
    id_categoria = models.IntegerField(primary_key=True)
    nombre = models.CharField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'categoriatrabajo'


class Comunidad(models.Model):
    id_comunidad = models.IntegerField(primary_key=True)
    id_distrito = models.ForeignKey('Distrito', models.DO_NOTHING, db_column='id_distrito', blank=True, null=True)
    nombre = models.CharField(blank=True, null=True)

    class Meta:
        db_table = 'comunidad'


class Denuncia(models.Model):
    id_denuncia = models.IntegerField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    id_empleador = models.ForeignKey('Empleador', models.DO_NOTHING, db_column='id_empleador', blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    estado = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = 'denuncia'


class Departamento(models.Model):
    id_departamento = models.IntegerField(primary_key=True)
    nombre = models.CharField(blank=True, null=True)

    class Meta:
        db_table = 'departamento'
    
    def __str__(self):
        return self.nombre


class Disponibilidad(models.Model):
    id_disponibilidad = models.IntegerField(primary_key=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'disponibilidad'


class Distrito(models.Model):
    id_distrito = models.IntegerField(primary_key=True)
    id_provincia = models.ForeignKey('Provincia', models.DO_NOTHING, db_column='id_provincia', blank=True, null=True)
    nombre = models.CharField(blank=True, null=True)

    class Meta:
        db_table = 'distrito'
    

class Empleador(models.Model):
    id_empleador = models.IntegerField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    nombre_empresa = models.CharField(blank=True, null=True)
    ruc = models.CharField(blank=True, null=True)
    verificado = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'empleador'


class Filtrotrabajoporzona(models.Model):
    id_filtro = models.IntegerField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    id_comunidad = models.ForeignKey(Comunidad, models.DO_NOTHING, db_column='id_comunidad', blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'filtrotrabajoporzona'


class Habilidad(models.Model):
    id_habilidad = models.IntegerField(primary_key=True)
    nombre = models.CharField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'habilidad'


class Ofertatrabajo(models.Model):
    id_oferta = models.IntegerField(primary_key=True)
    id_empleador = models.ForeignKey(Empleador, models.DO_NOTHING, db_column='id_empleador', blank=True, null=True)
    id_categoria = models.ForeignKey(Categoriatrabajo, models.DO_NOTHING, db_column='id_categoria', blank=True, null=True)
    titulo = models.CharField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    sueldo = models.FloatField(blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)

    class Meta:
        db_table = 'ofertatrabajo'


class Politicalegal(models.Model):
    id_politica = models.IntegerField(primary_key=True)
    nombre = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_actualizacion = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'politicalegal'


class Postulacion(models.Model):
    id_postulacion = models.IntegerField(primary_key=True)
    id_oferta = models.ForeignKey(Ofertatrabajo, models.DO_NOTHING, db_column='id_oferta', blank=True, null=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    estado = models.TextField(blank=True, null=True)
    fecha_postulacion = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'postulacion'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación con auth.User
    
    id_profile = models.AutoField(primary_key=True)
    id_usuario = models.OneToOneField('Usuario', models.DO_NOTHING, db_column='id_usuario')
    fecha_registro = models.DateTimeField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    foto_url = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)
    redes_sociales = models.JSONField(blank=True, null=True)
    id_comunidad = models.ForeignKey(Comunidad, models.DO_NOTHING, db_column='id_comunidad', blank=True, null=True)
    id_distrito = models.ForeignKey(Distrito, models.DO_NOTHING, db_column='id_distrito', blank=True, null=True)
    id_provincia = models.ForeignKey('Provincia', models.DO_NOTHING, db_column='id_provincia', blank=True, null=True)
    id_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='id_departamento', blank=True, null=True)
    categorias = models.TextField(blank=True, null=True)
    habilidades = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'profile'


class Provincia(models.Model):
    id_provincia = models.IntegerField(primary_key=True)
    id_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='id_departamento', blank=True, null=True)
    nombre = models.CharField(blank=True, null=True)

    class Meta:
        db_table = 'provincia'

        
class TrabajosRealizados(models.Model):
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    empresa = models.CharField(max_length=255, blank=True, null=True)
    rol = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'trabajos_realizados'


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil') #para mantener la personalizacion
    
    id_usuario = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, blank=False, null=False)
    nombres = models.CharField(blank=True, null=True)
    apellidos = models.CharField(blank=True, null=True)
    dni = models.CharField(blank=True, null=True)
    telefono = models.CharField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    clave = models.TextField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    sexo = models.CharField(blank=True, null=True)
    tipo_usuario = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_comunidad = models.ForeignKey(Comunidad, models.DO_NOTHING, db_column='id_comunidad', blank=True, null=True)
    habilitado = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'usuario'


class UsuarioCategoria(models.Model):
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    id_categoria = models.ForeignKey(Categoriatrabajo, models.DO_NOTHING, db_column='id_categoria')

    class Meta:
        db_table = 'usuario_categoria'
        unique_together = (('id_usuario', 'id_categoria'),)


class UsuarioHabilidad(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    id_habilidad = models.ForeignKey(Habilidad, models.DO_NOTHING, db_column='id_habilidad')

    class Meta:
        db_table = 'usuario_habilidad'
        unique_together = (('id_usuario', 'id_habilidad'),)



class Verificacion(models.Model):
    id_verificacion = models.IntegerField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    estado = models.TextField(blank=True, null=True)  # This field type is a guess.
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'verificacion'