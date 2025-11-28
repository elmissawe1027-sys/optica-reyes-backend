# api/urls.py

from django.urls import path
from . import views  # Importa las vistas (que aún no creamos)

urlpatterns = [
    # Cuando alguien llame a /api/registrar/
    path('registrar/', views.registrar_usuario, name='registrar'),

    # Cuando alguien llame a /api/login/
    path('login/', views.iniciar_sesion, name='login'),

    # Cuando alguien llame a /api/crear-pedido/
    path('crear-pedido/', views.crear_pedido, name='crear_pedido'),
    path('actualizar-perfil/', views.actualizar_perfil, name='actualizar_perfil'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
]