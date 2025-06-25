# capa de vista/presentación

from django.shortcuts import render, redirect
from .capas.servicios import servicios  # Asumo que esta capa abstrae acceso a la API
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos (si existe).
def home(request):
    imagenes = servicios.get_all_pokemons()  # función que accede a la API
    favourite_list = []

    if request.user.is_authenticated:
        favourite_list = servicios.get_favorites_by_user(request.user)

    return render(request, 'home.html', {
        'imagenes': imagenes,
        'favourite_list': favourite_list
    })

# función utilizada en el buscador.
def search(request):
    nombre = request.GET.get('consulta', '').lower()
    
    if nombre != '':
        imagenes = servicios.search_pokemon(nombre)
        favourite_list = []
        if request.user.is_authenticated:
            favourite_list = servicios.get_favorites_by_user(request.user)

        return render(request, 'home.html', {
            'imagenes': imagenes,
            'favourite_list': favourite_list
        })
    else:
        return redirect('home')

# función utilizada para filtrar por el tipo del Pokémon
def filter_by_type(request):
    tipo = request.GET.get('tipo', '').lower()

    if tipo != '':
        imagenes = servicios.filter_pokemon_by_type(tipo)
        favourite_list = []
        if request.user.is_authenticated:
            favourite_list = servicios.get_favorites_by_user(request.user)

        return render(request, 'home.html', {
            'imagenes': imagenes,
            'favourite_list': favourite_list
        })
    else:
        return redirect('home')

# Funciones protegidas para manejar favoritos
@login_required
def getAllFavouritesByUser(request):
    favoritos = servicios.get_favorites_by_user(request.user)
    return render(request, 'favourites.html', {
        'favourite_list': favoritos
    })

@login_required
def guardarFavorito(request):
    if request.method == 'POST':
        pokemon_id = request.POST.get('pokemon_id')
        servicios.add_favorite(request.user, pokemon_id)
    return redirect('home')

@login_required
def deleteFavorite(request):
    if request.method == 'POST':
        pokemon_id = request.POST.get('pokemon_id')
        servicios.remove_favorite(request.user, pokemon_id)
    return redirect('home')

@login_required
def salida(request):
    logout(request)
    return redirect('home')
