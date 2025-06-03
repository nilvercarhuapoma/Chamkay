from django.db import models
from django.conf import settings
from usuarios.models import Departamento, Provincia, Distrito, Comunidad



# Para usuarios 'ofrecer-trabajo' y 'ambos'
class OfertaUsuario(models.Model):
    empleador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo_usuario__in': ['ofrecer-trabajo', 'ambos']},
        related_name='ofertas_usuario'
    )
    titulo = models.CharField(max_length=255)
    pago = models.DecimalField(max_digits=10, decimal_places=2)
    horas_limite = models.TimeField()
    descripcion = models.TextField()
    herramientas = models.TextField()

    foto = models.ImageField(upload_to='ofertas/', blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField()

    id_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, null=True, blank=True)
    id_provincia = models.ForeignKey(Provincia, models.DO_NOTHING, null=True, blank=True)
    id_distrito = models.ForeignKey(Distrito, models.DO_NOTHING, null=True, blank=True)
    id_comunidad = models.ForeignKey(Comunidad, models.DO_NOTHING, null=True, blank=True)
    direccion_detalle = models.TextField(blank=True, null=True)

    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('vencida', 'Vencida'),
        ('completada', 'Completada'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activa')

    def __str__(self):
        return f"{self.titulo} - {self.empleador.email}"



# Para empresas (usuario con tipo_usuario='empresa')
class OfertaEmpresa(models.Model):
    empleador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo_usuario': 'empresa'},
        related_name='ofertas_empresa'
    )
    titulo_puesto = models.CharField(max_length=255)
    rango_salarial = models.CharField(max_length=100)
    experiencia_requerida = models.CharField(max_length=100)
    modalidad_trabajo = models.CharField(max_length=100)  # remoto/presencial/híbrido
    descripcion_puesto = models.TextField()
    requisitos_calificaciones = models.TextField()
    beneficios_compensaciones = models.TextField()
    numero_postulantes = models.PositiveIntegerField(default=0)

    foto = models.ImageField(upload_to='ofertas/', blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField()

    id_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, null=True, blank=True)
    id_provincia = models.ForeignKey(Provincia, models.DO_NOTHING, null=True, blank=True)
    id_distrito = models.ForeignKey(Distrito, models.DO_NOTHING, null=True, blank=True)
    id_comunidad = models.ForeignKey(Comunidad, models.DO_NOTHING, null=True, blank=True)
    direccion_detalle = models.TextField(blank=True, null=True)

    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('vencida', 'Vencida'),
        ('completada', 'Completada'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activa')

    def __str__(self):
        return f"{self.titulo_puesto} - {self.empleador.email}"


