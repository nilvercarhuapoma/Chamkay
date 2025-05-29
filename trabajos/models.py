from django.db import models

class Oferta(models.Model):
    id_empleador = models.IntegerField()  # Podrías usar ForeignKey si tienes el modelo Empleador
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_publicacion = models.DateField()
    fecha_limite = models.DateField()
    pago = models.DecimalField(max_digits=10, decimal_places=2)
    herramientas = models.TextField()
    
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('vencida', 'Vencida'),
        ('completada', 'Completada'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activa')

    def __str__(self):
        return self.titulo
