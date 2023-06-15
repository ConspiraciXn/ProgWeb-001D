from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static



# Importación de vistas o funciones.
from aplicacionWEb.views import *

urlpatterns = [

    # -----------------------------------------------------
    # Zona de administración
    # -----------------------------------------------------

    path('admin/', admin.site.urls),


    # -----------------------------------------------------
    # Sistema de autenticación
    # -----------------------------------------------------

    path('login/', inicio_sesion, name='inicio_sesion'),
    path('logout/', cierre_sesion, name='cierre_sesion'),
    path('registro/', registro_usuario, name='registro_usuario'),


    # -----------------------------------------------------
    # Vistas comunes
    # -----------------------------------------------------

    path('', inicio, name='inicio'), # ruta inicial, sin /.
    path('restringido/', restringido, name='restringido'), # ejemplo de proteccion de ruta


    # -----------------------------------------------------
    # CRUD de Pokemon
    # ----------------------------------------------------- 
    path('registro-pokemon/', registro_pokemon, name='registro_pokemon'),
    path('pokemon/', lista_pokemon, name='lista_pokemon'),
    path('detalle/', detalle_pokemon, name='detalle_pokemon'),


# Permitir servir recursos o archivos mediante los MEDIA.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
