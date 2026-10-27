from django.urls import path
from . import views
from django.contrib.auth.models import User

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name = 'registro'),
    path('favoritos/agregar/', views.agregra_favorito, name = 'agregar_favorito'),
    path('favoritos/', views.mis_favoritos, name = 'favoritos'),
    path('favoritos/quitar/<int:anime_id>/', views.quitar_favorito, name = 'quitar_favorito'),
    path('cerrar-sesion-navegador/', views.cerrar_sesion_navegador, name='cerrar_sesion_navegador'),
    path('usuarios/', views.listar_usuarios, name = 'listar_usuarios'),
    path('usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name = 'eliminar_usuario'),
    
    
]