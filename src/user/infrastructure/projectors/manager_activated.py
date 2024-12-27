import jsonpickle
from common.infrastructure.database.database import get_session
from common.infrastructure.database.mongo import get_mongo_client
from user.infrastructure.models.postgres.sqlalchemy.user_model import UserModel


def manager_activated_projector(ch, method, properties, body):
    
    mongo = get_mongo_client().__next__()
    
    event = jsonpickle.decode(body)
    
    db = mongo["template"]
    user_coll = db["user"]
    
    filter = {"id": str(event.manager_id.value)}
    
    update = {
        "$set": {
            "status": "ACTIVE",
        }
    }
    
    user_coll.update_one(filter, update, upsert=True)