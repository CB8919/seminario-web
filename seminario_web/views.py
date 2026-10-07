from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Favorito




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

        return r.json()['data']['Page']['media'], None

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