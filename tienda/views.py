from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime

from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
# Create your views here.
# -------------------------------------------------------------
def usuarioLogin(request):

    page = 'login'
    if request.method == 'POST':
        usuario = request.POST['usuario']
        contraseña = request.POST['contraseña']

        user = authenticate(request, username=usuario, password=contraseña)

        if user is not None:
            login(request,user)
            return redirect('tienda')

    return render(request, 'tienda/login.html',{'page':page})

# -------------------------------------------------------------
def usuarioLogout(request):
    logout(request)
    return redirect('tienda')

# -------------------------------------------------------------
def registrarUsuario(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            user = authenticate(request, username=user.username, password=request.POST['password1'])
            if user is not None:
                login(request, user)
                return redirect('tienda')

    context = {
        'form':form, 'page' : page
    }

    return render(request, 'tienda/login.html', context)

# -------------------------------------------------------------
def tienda(request):

    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, creado = Pedido.objects.get_or_create(cliente=cliente, completado=False)
        articulos = pedido.pedirarticulo_set.all()
        articulosCarrito = pedido.get_articulos_carrito
    else:
        articulos = []
        pedido = {'get_total_carrito':0, 'get_articulos_carrito':0, 'envio':False}
        articulosCarrito = pedido['get_articulos_carrito']

    productos = Producto.objects.all
    context = {
        'productos' : productos,
        'articulosCarrito' : articulosCarrito
    }
    return render(request, 'tienda/tienda.html', context)


# -------------------------------------------------------------
def carrito(request):

    # Autenticar
    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, creado = Pedido.objects.get_or_create(cliente=cliente, completado=False)
        articulos = pedido.pedirarticulo_set.all()
        articulosCarrito = pedido.get_articulos_carrito
    else:
        articulos = []
        pedido = {'get_total_carrito':0, 'get_articulos_carrito':0, 'envio':False}
        articulosCarrito = pedido['get_articulos_carrito']
    context = {
        'articulos': articulos,
        'pedido':pedido,
        'articulosCarrito' : articulosCarrito
    }
    return render(request, 'tienda/carrito.html', context)

 
# -------------------------------------------------------------
def checkout(request):
    # Autenticar
    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, creado = Pedido.objects.get_or_create(cliente=cliente, completado=False)
        articulos = pedido.pedirarticulo_set.all()
        articulosCarrito = pedido.get_articulos_carrito
    else:
        articulos = []
        pedido = {'get_total_carrito':0, 'get_articulos_carrito':0, 'envio':False}
        articulosCarrito = pedido['get_articulos_carrito']
    context = {
        'articulos': articulos,
        'pedido':pedido,
        'articulosCarrito':articulosCarrito
    }

    return render(request, 'tienda/checkout.html', context)

# -------------------------------------------------------------
def actualizarArticulo(request):
    data = json.loads(request.body)
    productoId = data['productoId']
    action = data['action']

    print('Action:', action)
    print('productoId:', productoId)

    cliente = request.user.cliente
    producto = Producto.objects.get(id=productoId)
    pedido, creado = Pedido.objects.get_or_create(cliente=cliente, completado=False)

    pedidoArticulo, creado = PedirArticulo.objects.get_or_create(pedido=pedido, producto=producto)

    if action == 'add':
        pedidoArticulo.cantidad = (pedidoArticulo.cantidad + 1)
    elif action == 'remove':
        pedidoArticulo.cantidad = (pedidoArticulo.cantidad -1)
    elif action == 'delete':
        pedidoArticulo.delete()
        return JsonResponse('Articulo eliminado', safe=False)

    pedidoArticulo.save()

    if pedidoArticulo.cantidad <= 0:
        pedidoArticulo.delete()
    
    
    return JsonResponse('Articulo fue agregado', safe=False)


# -------------------------------------------------------------
def procesarPedido(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if (request.user.is_authenticated):
        cliente = request.user.cliente
        pedido, creado = Pedido.objects.get_or_create(cliente=cliente, completado=False)
        total = float(data['form']['total'])
        pedido.id_transaccion = transaction_id

        if total == pedido.get_total_carrito:
            pedido.completado = True
        pedido.save()

        if pedido.envio == True:
            DireccionEnvio.objects.create(
                cliente = cliente,
                pedido = pedido,
                direccion = data['envio']['address'],
                ciudad = data['envio']['city'],
                estado = data['envio']['state'],
                codigopostal = data['envio']['zipcode'],
            )

    else:
        print('Sesion no iniciada..')
    return JsonResponse('Pago Completado!', safe=False)

