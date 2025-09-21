# db_mongo.py
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


def inserir_local(local):
    """Insere um documento local no MongoDB"""
    collection = get_collection()
    return collection.insert_one(local).inserted_id

def listar_locais_por_cidade(cidade):
    """Retorna todos os locais de uma cidade"""
    collection = get_collection()
    return list(collection.find({"cidade": cidade}))

def deletar_local(local_id):
    """Deleta um local pelo _id"""
    collection = get_collection()
    return collection.delete_one({"_id": local_id})

def atualizar_local(local_id, dados):
    """Atualiza um local pelo _id"""
    collection = get_collection()
    return collection.update_one({"_id": local_id}, {"$set": dados})

def listar_locais():
    """Retorna todos os locais"""
    collection = get_collection()
    return list(collection.find())