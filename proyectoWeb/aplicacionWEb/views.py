from .models import *

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout     # para autenticacion
from django.contrib.auth.decorators import login_required   # para proteccion de rutas
from django.contrib.auth.models import User                 # importar usuario Django



# -----------------------------------------------------
# Sistema de autenticación
# -----------------------------------------------------

def inicio_sesion(request):

    # Recibir informacion del formulario de la template.
    if request.method == "POST":
        
        usuario = request.POST.get("txtUsuario") # el texto entre comillas es el name del input.
        contrasena = request.POST.get("txtContrasena")

        autenticacion = authenticate(request, username=usuario, password=contrasena)

        if autenticacion is not None:
            login(request, autenticacion)
            return redirect('/')    # redirigir al home

    return render(request, "inicio_sesion.html")

def cierre_sesion(request):

    # Función para eliminar o cerrar la sesión del usuario.
    logout(request)
    return redirect('/login/')  # redirige al login.

def registro_usuario(request):

    # Validar si existen datos mediante POST.
    if request.method == "POST":

        # Obtener data del formulario.
        nombre = request.POST.get("txtNombre")
        apellido = request.POST.get("txtApellido")
        usuario = request.POST.get("txtUsuario")
        email = request.POST.get("txtEmail")
        contrasena = request.POST.get("txtContrasena")

        # Crear usuario y asignar atributos.
        usuario = User.objects.create_user(usuario, email, contrasena)
        usuario.save()

        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.save()
       
        return redirect('/')

    return render(request, "registro_usuario.html")


# -----------------------------------------------------
# Vistas comunes
# -----------------------------------------------------

def inicio(request):

    # Traer los pokemon de la BD.
    pokemon = Pokemon.objects.all()

    contexto = {
        "lista_pokemon" : pokemon
    }
    return render(request, "home.html", contexto)

@login_required(login_url='/login/')
def restringido(request):
    return render(request, "restringido.html")



# -----------------------------------------------------
# CRUD de Pokemon
# -----------------------------------------------------

def registro_pokemon(request):

    # Validar si hay una consulta POST.
    if request.method == "POST":

        # Obtener data del POST.
        nombre = request.POST.get("txtNombre")
        categoria = request.POST.get("txtCategoria")
        tipo = request.POST.get("txtTipo")
        valor = request.POST.get("txtValor")

        imagen = request.FILES['inputImagen']

        # Crear objeto Pokemon.
        pokemon = Pokemon()
        pokemon.nombre = nombre
        pokemon.categoria = categoria
        pokemon.tipo = tipo
        pokemon.valor = valor
        pokemon.imagen = imagen
        pokemon.save()

        return redirect('/')

    return render(request, "registro_pokemon.html")

def lista_pokemon(request):

    # Traer los pokemon de la BD.
    pokemon = Pokemon.objects.all()

    contexto = {
        "lista_pokemon" : pokemon
    }
    return render(request, "lista_pokemon.html", contexto)


def detalle_pokemon(request):
    return render(request, "detalle_pokemon.html")


