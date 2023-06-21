from django.db import models
from django.contrib.auth.models import User                 # importar usuario Django

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
    

class CarritoCompra(models.Model):

    comprador = models.ForeignKey(User, on_delete=models.CASCADE)
    subtotal = models.IntegerField()
    descuento = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return "Carrito de " + str(self.comprador.username)


class ItemCarrito(models.Model):

    carrito = models.ForeignKey(CarritoCompra, on_delete=models.CASCADE)
    producto_original = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    valor = models.IntegerField()

    def __str__(self):
        return str(self.carrito.comprador.username) + " / " + str(self.producto_original.nombre)

