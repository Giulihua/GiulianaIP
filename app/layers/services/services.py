from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokémon
def getAllImages():
    # 1) Traer datos crudos de la API
    raw_pokemons = transport.get_all_pokemons()

    # 2) Convertirlos en objetos Card (usando el traductor)
    cards = []
    for raw in raw_pokemons:
        card = translator.raw_to_card(raw)
        cards.append(card)

    # 3) Devolver listado de cards
    return cards

# función que filtra según el nombre del Pokémon.
def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():
        if name.lower() in card.name.lower():
            filtered_cards.append(card)

    return filtered_cards

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []

    for card in getAllImages():
        if type_filter.lower() in [t.lower() for t in card.types]:
            filtered_cards.append(card)

    return filtered_cards

# Añadir favorito (usado desde el template 'home.html')
def saveFavourite(request):
    fav = translator.request_to_favourite(request)  # transforma request en Card
    fav.user = get_user(request)
    return repositories.save_favourite(fav)

# Obtener todos los favoritos del usuario (usado desde 'favourites.html')
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)
        favourite_list = repositories.get_favourites_by_user(user)
        mapped_favourites = []

        for favourite in favourite_list:
            card = translator.favourite_to_card(favourite)
            mapped_favourites.append(card)

        return mapped_favourites

# Eliminar favorito por ID
def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId)

# obtener el ícono del tipo (opcional para decorar el template)
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)
