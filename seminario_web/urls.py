from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name = 'registro'),
    path('favoritos/agregar/', views.agregra_favorito, name = 'agregar_favorito'),
    path('favoritos/', views.mis_favoritos, name = 'favoritos'),
    path('favoritos/quitar/<int:anime_id>/', views.quitar_favorito, name = 'quitar_favorito'),
    
    
]