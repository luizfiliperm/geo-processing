import os
from pymongo import MongoClient
from bson import ObjectId


class LocalService:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        client = MongoClient(mongo_uri)
        db = client["projeto_poliglota"]
        self.collection = db["locais"]

    def insert_place(self, place: dict):
        """Insert a new place into MongoDB"""
        return self.collection.insert_one(place).inserted_id

    def get_places_by_city(self, city: str):
        """Return all places for a given city"""
        return list(self.collection.find({"cidade": city}))

    def delete_place(self, place_id: str):
        """Delete a place by its _id"""
        return self.collection.delete_one({"_id": ObjectId(place_id)})

    def update_place(self, place_id: str, data: dict):
        """Update a place by its _id"""
        return self.collection.update_one({"_id": ObjectId(place_id)}, {"$set": data})

    def get_all_places(self):
        """Return all places"""
        return list(self.collection.find())

    def get_nearby_places(self, latitude: float, longitude: float, raio_km: float = 10):
        """Return places within a radius (km) of the given coordinates"""
        from geoprocessing import distance_km
        all_places = list(self.collection.find())
        result = []
        for p in all_places:
            coord_place = (p["coordenadas"]["latitude"], p["coordenadas"]["longitude"])
            if distance_km((latitude, longitude), coord_place) <= raio_km:
                result.append(p)
        return result
