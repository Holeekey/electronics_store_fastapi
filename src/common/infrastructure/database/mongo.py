from pymongo import MongoClient
from config import MONGO_URL

from di.dependent import Injectable


def get_mongo_client():
    client = MongoClient(MONGO_URL)
    try:
        yield client
    finally:
        pass


class MongoSession(Injectable, scope="request"):

    def __init__(self):
        self._session = get_mongo_client().__next__()

    @property
    def session(self):
        return self._session
