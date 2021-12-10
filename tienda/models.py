from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200, null=True)
    precio = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    imagen = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    @property
    def imagenURL(self):
        try:
            url = self.imagen.url
        except:
            url = 'images/placeholder.png'
        return url


class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False, null=True, blank=False)
    id_transaccion = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def envio(self):
        envio = False
        articulosPedido = self.pedirarticulo_set.all()
        for i in articulosPedido:
            if i.producto.digital == False:
                envio = True

        return envio

    @property
    def get_total_carrito(self):
        articulospedido = self.pedirarticulo_set.all()
        total = sum([articulo.get_total for articulo in articulospedido])
        return total
 
    @property
    def get_articulos_carrito(self):
        articulospedido = self.pedirarticulo_set.all()
        total = sum([articulo.cantidad for articulo in articulospedido])
        return total



class PedirArticulo(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, blank=True, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, blank=True, null=True)
    cantidad = models.IntegerField(default=0, null=True, blank=True)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.producto.precio * self.cantidad
        return total


class DireccionEnvio(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, blank=True, null=True)
    direccion = models.CharField(max_length=200, null=True)
    ciudad = models.CharField(max_length=200, null=True)
    estado = models.CharField(max_length=200, null=True)
    codigopostal = models.CharField(max_length=200, null=True)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.direccion