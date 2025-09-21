# src/geoprocessamento.py
from geopy.distance import geodesic
from db_mongo import get_collection

def distancia_km(coord1, coord2):
    """
    Calcula a distância em km entre duas coordenadas.
    coord1 e coord2 = (latitude, longitude)
    """
    return geodesic(coord1, coord2).km

def locais_proximos(latitude, longitude, raio_km=10):
    """
    Retorna locais do MongoDB dentro de um raio (em km) da coordenada fornecida.
    """
    collection = get_collection()
    todos_locais = list(collection.find())
    resultado = []

    for l in todos_locais:
        coord_local = (l["coordenadas"]["latitude"], l["coordenadas"]["longitude"])
        if distancia_km((latitude, longitude), coord_local) <= raio_km:
            resultado.append(l)
    return resultado
