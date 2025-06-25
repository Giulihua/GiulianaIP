import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# ========== Servicios dentro del mismo archivo ==========

def get_all_pokemons(limit=20):
    url = f'https://pokeapi.co/api/v2/pokemon?limit={limit}'
    response = requests.get(url)
    results = response.json().get('results', [])

    pokemons = []

    for p in results:
        data = requests.get(p['url']).json()
        pokemons.append({
            'id': data['id'],
            'name': data['name'].capitalize(),
            'image': data['sprites']['front_default'],
            'types': [t['type']['name'].capitalize() for t in data['types']],
            'height': data['height'],
            'weight': data['weight'],
            'base_experience': data['base_experience'],
        })

    return pokemons

def search_pokemon(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name.lower()}'
    response = requests.get(url)
    if response.status_code != 200:
        return []

    data = response.json()
    return [{
        'id': data['id'],
        'name': data['name'].capitalize(),
        'image': data['sprites']['front_default'],
        'types': [t['type']['name'].capitalize() for t in data['types']],
        'height': data['height'],
        'weight': data['weight'],
        'base_experience': data['base_experience'],
    }]

def filter_pokemon_by_type(tipo):
    url = f'https://pokeapi.co/api/v2/type/{tipo.lower()}'
    response = requests.get(url)
    if response.status_code != 200:
        return []

    results = response.json()['pokemon']
    pokemons = []

    for p in results[:20]:
        data = requests.get(p['pokemon']['url']).json()
        pokemons.append({
            'id': data['id'],
            'name': data['name'].capitalize(),
            'image': data['sprites']['front_default'],
            'types': [t['type']['name'].capitalize() for t in data['types']],
            'height': data['height'],
            'weight': data['weight'],
            'base_experience': data['base_experience'],
        })
    return pokemons

# Simulamos favoritos (no implementados)
def get_favorites_by_user(user):
    return []

def add_favorite(user, pokemon_id):
    pass

def remove_favorite(user, pokemon_id):
    pass

# ========== Vistas ==========

def index_page(request):
    return render(request, 'index.html')

def home(request):
    imagenes = get_all_pokemons()
    favourite_list = []
    if request.user.is_authenticated:
        favourite_list = get_favorites_by_user(request.user)

    return render(request, 'home.html', {
        'imagenes': imagenes,
        'favourite_list': favourite_list
    })

def search(request):
    nombre = request.GET.get('consulta', '')
    if nombre:
        imagenes = search_pokemon(nombre)
        favourite_list = []
        if request.user.is_authenticated:
            favourite_list = get_favorites_by_user(request.user)

        return render(request, 'home.html', {
            'imagenes': imagenes,
            'favourite_list': favourite_list
        })
    return redirect('home')

def filter_by_type(request):
    tipo = request.GET.get('tipo', '')
    if tipo:
        imagenes = filter_pokemon_by_type(tipo)
        favourite_list = []
        if request.user.is_authenticated:
            favourite_list = get_favorites_by_user(request.user)

        return render(request, 'home.html', {
            'imagenes': imagenes,
            'favourite_list': favourite_list
        })
    return redirect('home')

@login_required
def getAllFavouritesByUser(request):
    favoritos = get_favorites_by_user(request.user)
    return render(request, 'favourites.html', {
        'favourite_list': favoritos
    })

@login_required
def guardarFavorito(request):
    if request.method == 'POST':
        pokemon_id = request.POST.get('pokemon_id')
        add_favorite(request.user, pokemon_id)
    return redirect('home')

@login_required
def deleteFavorite(request):
    if request.method == 'POST':
        pokemon_id = request.POST.get('pokemon_id')
        remove_favorite(request.user, pokemon_id)
    return redirect('home')

@login_required
def salida(request):
    logout(request)
    return redirect('home')
