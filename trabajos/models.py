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
    
    
class Trabajo(models.Model): #solo es para que me funcione perfil :)
    # no importes Usuario al inicio
    
    # luego en el ForeignKey usa string con el app label + modelo:
    trabajador = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='trabajos_realizados')
    cliente = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='trabajos_contratados')

    # resto del modelo...