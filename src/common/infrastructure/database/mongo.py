from pymongo import MongoClient
from config import MONGO_URL

from di.dependent import Injectable

client = MongoClient(MONGO_URL)

def get_mongo_client():
    try:
        yield client
    finally:
        client.close()
        
class MongoSession(Injectable, scope="request"):
    
    def __init__(self):
        self._session = get_mongo_client().__next__()
        
    @property
    def session(self):
        return self._session