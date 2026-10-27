import html
import re

from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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


@login_required # Sirve para que solo los usuarios autenticados puedan acceder a la vista
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

@login_required
def quitar_favorito(request, anime_id):
    if request.method == 'POST':
        Favorito.objects.filter(user = request.user, anime_id = anime_id).delete()
    return redirect('favoritos')


@csrf_exempt
def cerrar_sesion_navegador(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'ok': True})

    return JsonResponse({'ok': False}, status=405)

@staff_member_required
def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'registration/usuarios.html', {'usuarios': usuarios})

@staff_member_required
@require_POST
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    if usuario != request.user:
        usuario.delete()

    return redirect('listar_usuarios')


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
            return render(request, 'consulta.html', {
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