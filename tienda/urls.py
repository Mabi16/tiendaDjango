from django.urls import path
from . import views

urlpatterns = [
    path('', views.tienda, name="tienda"),
    path('carrito/', views.carrito, name="carrito"),
    path('checkout/', views.checkout, name="checkout"),
    
    path('iniciar/', views.usuarioLogin, name="inicio_sesion"),
    path('cerrar/', views.usuarioLogout, name="cierre_sesion"),
    path('registrar/', views.registrarUsuario, name="registro"),


    path('actualizar_articulo/', views.actualizarArticulo, name="actualizar_articulo"),
    path('procesar_pedido/', views.procesarPedido, name="procesar_pedido"),
]
