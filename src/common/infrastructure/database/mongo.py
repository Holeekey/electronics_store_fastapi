from pymongo import MongoClient

from src.config import MONGO_URL

client = MongoClient(MONGO_URL)

def get_mongo_client():
    try:
        yield client
    finally:
        pass