import html
import re
from django.contrib.auth import logout
from django.http import JsonResponse
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from .models import Favorito, Consulta
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django import forms



class ActualizarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

def limpiar_sinopsis(description):
    if not isinstance(description, str):
        return ''

    description = re.sub(
        r'<\s*br\s*/?\s*>|</\s*(?:p|div|li|h[1-6])\s*>',
        '\n',
        description,
        flags=re.IGNORECASE,
    )
    return html.unescape(strip_tags(description)).strip()


# Función para manejar el registro de usuarios

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def actualizar_usuario(request):
    if request.method == 'POST':
        form = ActualizarUsuarioForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = ActualizarUsuarioForm(instance=request.user)

    return render(
        request,
        'registration/actualizar_usuario.html',
        {'form': form}
    )

# Función para obtener los animes desde la API de Anilist

def obtener_animes(page=1):
    query = """
query ($page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    media(
      type: ANIME,
      status: RELEASING,
      sort: TRENDING_DESC
    ) {
      id
      title {
        romaji
      }
      coverImage {
        large
      }
      episodes
      description(asHtml: false)
      trailer {
        id
        site
        thumbnail
      }
    }
  }
}
"""

    variables = {
        "page": page,
        "perPage": 10,
    }

    try:
        r = requests.post(
            'https://graphql.anilist.co',
            json={
                'query': query,
                'variables': variables
            },
            timeout=10
        )

        r.raise_for_status()

        animes = r.json()['data']['Page']['media']
        for anime in animes:
            anime['description'] = limpiar_sinopsis(anime.get('description'))

        return animes, None

    except (requests.RequestException, KeyError):
        return [], 'No se pudo cargar la lista de animes.'

# Vista para la página de inicio, que muestra los animes obtenidos desde la API de Anilist

def inicio(request):
    animes, error = [], None

    if request.user.is_authenticated:
        pagina = int(request.GET.get('pagina', 1))
        animes, error = obtener_animes(pagina)

    return render(
        request,
        'inicio.html',
        {
            'animes': animes,
            'error': error,
            'pagina': pagina if request.user.is_authenticated else 1,
        }
    )

# Vista para agregar un anime a los favoritos del usuario autenticado
@login_required 
def agregra_favorito(request):
    if request.method == 'POST':
        Favorito.objects.get_or_create(
            user = request.user,
            anime_id = request.POST['anime_id'],
            defaults = {
                'titulo': request.POST['titulo'],
                'imagen': request.POST['imagen'],
            },
        )
    return redirect('inicio')

# Agrega la vista para mostrar los favoritos del usuario autenticado
@login_required
def mis_favoritos(request):
    favoritos = Favorito.objects.filter(user = request.user)
    return render(request, 'favoritos.html', {'favoritos': favoritos})


# Vista para quitar un anime de los favoritos del usuario autenticado
@login_required
def quitar_favorito(request, anime_id):
    if request.method == 'POST':
        Favorito.objects.filter(user = request.user, anime_id = anime_id).delete()
    return redirect('favoritos')


# Vista para cerrar la sesión del usuario autenticado y devolver una respuesta JSON
@require_POST
@login_required
def cerrar_sesion_navegador(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'ok': True})

    return JsonResponse({'ok': False}, status=405)

# Vista para listar todos los usuarios registrados, accesible solo para miembros del personal
@staff_member_required
def listar_usuarios(request):
    usuarios = User.objects.all()

        
    return render(request, 'registration/usuarios.html', {'usuarios': usuarios})

# Vista para eliminar un usuario, accesible solo para miembros del personal
@staff_member_required
@require_POST
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    if usuario != request.user:
        usuario.delete()

    return redirect('listar_usuarios')

# Vista para enviar consultas, accesible solo para usuarios autenticados
@login_required
def enviar_consulta(request):
    if request.method == 'POST':
        asunto = request.POST.get('asunto', '').strip()
        mensaje = request.POST.get('mensaje', '').strip()

        asuntos_validos = [
            'Consulta sobre la web',
            'Problema con mi cuenta',
            'Sugerencia',
            'Otro',
        ]

        if asunto not in asuntos_validos or not mensaje:
            return render(request, 'registration/consulta.html', {
                'error': 'Completá el asunto y el mensaje correctamente.',
            })

        Consulta.objects.create(
            usuario=request.user,
            asunto=asunto,
            mensaje=mensaje,
        )

        return render(request, 'registration/consulta.html', {
            'enviado': True,
        })

    return render(request, 'registration/consulta.html')

# Vista para la página "Nosotros"
def nosotros(request):
    return render(request, 'nosotros.html')