from django.urls import path
from . import views
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name = 'registro'),
    path('mi-cuenta/', views.actualizar_usuario, name='actualizar_usuario'),
    path(
    'mi-cuenta/cambiar-password/',
    PasswordChangeView.as_view(
        template_name='registration/cambiar_password.html',
        success_url='/'
    ),
    name='cambiar_password'
),
    path('favoritos/agregar/', views.agregra_favorito, name = 'agregar_favorito'),
    path('favoritos/', views.mis_favoritos, name = 'favoritos'),
    path('favoritos/quitar/<int:anime_id>/', views.quitar_favorito, name = 'quitar_favorito'),
    path('cerrar-sesion-navegador/', views.cerrar_sesion_navegador, name='cerrar_sesion_navegador'),
    path('usuarios/', views.listar_usuarios, name = 'listar_usuarios'),
    path('usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name = 'eliminar_usuario'),
    path('consulta/', views.enviar_consulta, name = 'consulta'),
    path('nosotros/', views.nosotros, name = 'nosotros'),
    
]