from .models import *

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout     # para autenticacion
from django.contrib.auth.decorators import login_required   # para proteccion de rutas
from django.contrib.auth.models import User                 # importar usuario Django



# -----------------------------------------------------
# Funciones personalizadsa
# -----------------------------------------------------

def es_administrador(id_usuario) -> bool:
    """ Validar si un usuario es administrador,
    retorna un booleano."""

    usuario = User.objects.get(id = id_usuario)
    
    if usuario.is_staff:
        return True

    else:
        return False



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

@login_required(login_url='/login/')
def registro_pokemon(request):

    # Validar si es administrador.
    validacion = es_administrador(request.user.id)
    if validacion: # if validacion == True:

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
    
    else:
        return redirect(to='/')

@login_required(login_url='/login/')
def lista_pokemon(request):

    # Validar si es administrador.
    validacion = es_administrador(request.user.id)
    if validacion: # if validacion == True:

        # Traer los pokemon de la BD.
        pokemon = Pokemon.objects.all()

        contexto = {
            "lista_pokemon" : pokemon
        }
        return render(request, "lista_pokemon.html", contexto)
    
    else:
        return redirect(to='/')

@login_required(login_url='/login/')
def detalle_pokemon(request, id_pokemon):

    # Validar si es administrador.
    validacion = es_administrador(request.user.id)
    if validacion: # if validacion == True:

        pokemon = Pokemon.objects.get(id = id_pokemon)

        contexto = {
            "pokemon": pokemon
        }
        return render(request, "detalle_pokemon.html", contexto)

    else:
        return redirect(to='/')
    


# -----------------------------------------------------
# Carrito de compra
# -----------------------------------------------------

@login_required(login_url='/login/')
def carrito_compra(request):

    validacion_carrito = CarritoCompra.objects.filter(comprador = request.user)
    
    # Validar si existe un carrito.
    if len(validacion_carrito) > 0:
        carrito_existe = True

        carrito = CarritoCompra.objects.get(comprador = request.user)
        lista_productos = ItemCarrito.objects.filter(carrito = carrito)

        contexto = {
            "carrito": carrito,
            "lista_productos": lista_productos,
            "carrito_existe": carrito_existe
        }
        return render(request, 'carrito.html', contexto)

    # Si no existe, no retornarlo.
    else:
        carrito_existe = False
        contexto = {
            "carrito_existe": carrito_existe
        }
        return render(request, 'carrito.html', contexto)

@login_required(login_url='/login/')
def agregar_prod_carrito(request, id_producto):

    # Obtener producto.
    producto = Pokemon.objects.get(id = id_producto)

    # Validar si ya existe un carrito.
    validacion_carrito = CarritoCompra.objects.filter(comprador = request.user)
    
    # Si el carrito ya existe, se trae.
    if len(validacion_carrito) > 0:

        # Traer carrito existente.
        carrito = CarritoCompra.objects.get(comprador = request.user)

    # Si el carrito no existe, se crea.
    else:

        # Crear carrito de compra.
        carrito = CarritoCompra()
        carrito.comprador = request.user
        carrito.subtotal = 0
        carrito.descuento = 0
        carrito.total = 0
        carrito.save()

    # Validar existencia de producto en carrito.
    validacion_producto = ItemCarrito.objects.filter(carrito = carrito).filter(producto_original = producto)

    # Si el producto ya existe, aumentamos cantidad.
    if len(validacion_producto) > 0:

        item = ItemCarrito.objects.get(carrito = carrito, producto_original = producto)
        item.cantidad += 1
        item.save()

    # Si el producto no existe, lo creamos.
    else:
        
        # Crear item de carrito.
        item = ItemCarrito()
        item.carrito = carrito
        item.producto_original = producto
        item.cantidad = 1
        item.valor = producto.valor
        item.save()
    
    # Actualizar valores de carrito.
    carrito.subtotal += item.valor
    carrito.descontal = 0
    carrito.total += item.valor
    carrito.save()

    # Funcion inicio:
    # Traer los pokemon de la BD.
    pokemon = Pokemon.objects.all()

    contexto = {
        "lista_pokemon" : pokemon,
        "alerta_carrito": True
    }
    return render(request, "home.html", contexto)

@login_required(login_url='/login/')
def aumentar_cant_carrito(request, id_producto):

    # Obtener producto.
    producto = ItemCarrito.objects.get(id = id_producto)
    producto.cantidad += 1
    producto.save()

    # Actualizar carrito.
    carrito = producto.carrito
    carrito.subtotal += producto.valor
    carrito.total += producto.valor
    carrito.save()

    return redirect('/mi-carrito/')


@login_required(login_url='/login/')
def disminuir_cant_carrito(request, id_producto):

    # Obtener producto.
    producto = ItemCarrito.objects.get(id = id_producto)
    producto.cantidad -= 1
    producto.save()

    # Validar si cantidad es 0 o menos.
    if producto.cantidad <= 0:
        producto.delete()

    # Actualizar carrito.
    carrito = producto.carrito
    carrito.subtotal -= producto.valor
    carrito.total -= producto.valor
    carrito.save()

    return redirect('/mi-carrito/')


@login_required(login_url='/login/')
def eliminar_producto_carrito(request, id_producto):

    # Obtener producto.
    producto = ItemCarrito.objects.get(id = id_producto)

    # Actualizar carrito.
    carrito = producto.carrito
    carrito.subtotal -= producto.valor * producto.cantidad
    carrito.total -= producto.valor * producto.cantidad
    carrito.save()

    # Eliminar item de producto.
    producto.delete()
    
    return redirect('/mi-carrito/')


@login_required(login_url='/login/')
def finalizar_compra(request, id_carrito):

    # Obtener carrito.
    carrito = CarritoCompra.objects.get(id = id_carrito)
    carrito.delete()
    
    return redirect('/mi-carrito/')

