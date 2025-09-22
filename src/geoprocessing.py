from geopy.distance import geodesic
from db_mongo import get_collection

def distance_km(coord1, coord2):
    """
    Calcula a distância em km entre duas coordenadas.
    coord1 e coord2 = (latitude, longitude)
    """
    return geodesic(coord1, coord2).km

from db_mongo import get_collection
import math

def get_nearby_places(latitude, longitude, radius_km=10):
    collection = get_collection()
    
    query = {
        "$expr": { #serve pra calcular a distância aproximada dentro do MongoDB retornando só os documentos que estão dentro do raio
            "$lte": [
                {
                    "$sqrt": {
                        "$add": [
                            {"$pow": [{"$subtract": ["$coordenadas.latitude", latitude]}, 2]},
                            {"$pow": [{"$subtract": ["$coordenadas.longitude", longitude]}, 2]}
                        ]
                    }
                },
                radius_km / 111  
            ]
        }
    }
    return list(collection.find(query))
