from django.contrib.auth.models import AbstractUser
from django.db import models

class Calle(models.Model):
    id_calle = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'calle'

class Distrito(models.Model):
    id_distrito = models.IntegerField(primary_key=True)
    nombre = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'distrito'

class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'departamento'
        
class Provincia(models.Model):
    id_provincia = models.AutoField(primary_key=True)
    nombre = models.CharField(blank=True, null=True)
    id_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='id_departamento', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'provincia'




class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
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
    habilitado = models.BooleanField(blank=True, null=True)
    id_provincia = models.ForeignKey(Provincia, models.DO_NOTHING, db_column='id_provincia', blank=True, null=True)
    id_distrito = models.ForeignKey(Distrito, models.DO_NOTHING, db_column='id_distrito', blank=True, null=True)
    id_calle = models.ForeignKey(Calle, models.DO_NOTHING, db_column='id_calle', blank=True, null=True)
    id_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='id_departamento', blank=True, null=True)    

    class Meta:
        managed = False
        db_table = 'usuario'
