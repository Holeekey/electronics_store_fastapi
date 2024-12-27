import jsonpickle
from common.infrastructure.database.database import get_session
from common.infrastructure.database.mongo import get_mongo_client
from user.infrastructure.models.postgres.sqlalchemy.user_model import UserModel


def client_suspended_projector(ch, method, properties, body):
    
    mongo = get_mongo_client().__next__()
    
    event = jsonpickle.decode(body)
    
    db = mongo["template"]
    user_coll = db["user"]
    
    filter = {"id": str(event.client_id.value)}
    
    update = {
        "$set": {
            "status": "SUSPENDED",
        }
    }
    
    user_coll.update_one(filter, update, upsert=True)