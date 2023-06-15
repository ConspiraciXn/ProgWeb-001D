from django.db import models

# Creación de modelos para Base de Datos.

class Pokemon(models.Model):

    # ID son creados automáticamente.
    nombre = models.CharField(max_length=50, blank=True)
    categoria = models.CharField(max_length=50, blank=True)
    tipo = models.CharField(max_length=50, blank=True)
    imagen = models.ImageField(upload_to='imagen_pokemon/') # campo Imagen requiere libreria Pillow
    valor = models.IntegerField(null=True)

    def __str__(self):
        return self.nombre