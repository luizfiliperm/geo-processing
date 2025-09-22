import os
from pymongo import MongoClient

def get_client():
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(MONGO_URI)
    return client

def get_collection():
    client = get_client()
    db = client["projeto_poliglota"]
    return db["locais"]

