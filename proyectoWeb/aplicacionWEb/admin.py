from django.contrib import admin
from .models import *

# Register your models here.

class PokemonAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'categoria', 'tipo', 'valor']   # Campos que se mostrarán.
    ordering = ['id']                                           # Ordenar la lista por nombre.
    search_fields = ['nombre', 'tipo', 'categoria']                 # Permitir búsqueda por nombre.
    list_per_page = 10                                       # Cuántos elementos se ven por página.
    list_filter = ['categoria', 'tipo',]                    # Permitir filtrar elementos.
    #list_editable = ['nombre', 'categoria', 'tipo', 'valor']  # Permite modificar campos directamente.

admin.site.register(Pokemon, PokemonAdmin)

admin.site.register(ItemCarrito)
admin.site.register(CarritoCompra)