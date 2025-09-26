import os
from pymongo import MongoClient
from bson import ObjectId
from geoprocessing import distance_km

class PlaceService:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        client = MongoClient(mongo_uri)
        db = client["polyglot_project"]
        self.collection = db["places"]

    def _map_document(self, doc):
        """Mapear campos antigos em português para campos em inglês"""
        return {
            "_id": doc["_id"],
            "place_name": doc.get("place_name") or doc.get("nome_local", ""),
            "city": doc.get("city") or doc.get("cidade", ""),
            "coordinates": doc.get("coordinates") or doc.get("coordenadas", {"latitude": 0, "longitude": 0}),
            "description": doc.get("description") or doc.get("descricao", "")
        }

    def insert_place(self, place: dict):
        """Inserir um novo local no MongoDB"""
        return self.collection.insert_one(place).inserted_id

    def get_places_by_city(self, city: str):
        """Retornar todos os locais de uma determinada cidade"""
        docs = list(self.collection.find({"$or": [{"city": city}, {"cidade": city}]}))
        return [self._map_document(d) for d in docs]

    def delete_place(self, place_id: str):
        """Deletar um local pelo seu _id"""
        return self.collection.delete_one({"_id": ObjectId(place_id)})

    def update_place(self, place_id: str, data: dict):
        """Atualizar um local pelo seu _id"""
        return self.collection.update_one({"_id": ObjectId(place_id)}, {"$set": data})

    def get_all_places(self):
        """Retornar todos os locais"""
        docs = list(self.collection.find())
        return [self._map_document(d) for d in docs]

    def get_nearby_places(self, latitude: float, longitude: float, radius_km: float = 10):
        """Retornar locais dentro de um raio (km) das coordenadas fornecidas"""
        docs = list(self.collection.find())
        result = []
        for d in docs:
            coords = d.get("coordinates") or d.get("coordenadas", {"latitude": 0, "longitude": 0})
            coord_place = (coords["latitude"], coords["longitude"])
            if distance_km((latitude, longitude), coord_place) <= radius_km:
                result.append(self._map_document(d))
        return result
