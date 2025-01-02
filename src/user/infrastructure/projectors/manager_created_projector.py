from bson import ObjectId
import jsonpickle

from common.infrastructure.database.database import get_session
from common.infrastructure.database.mongo import get_mongo_client
from user.infrastructure.models.postgres.sqlalchemy.user_model import UserModel

def manager_created_projector(ch, method, properties, body):
    
    mongo = get_mongo_client().__next__()
    db_sesion = get_session().__next__()
    
    event = jsonpickle.decode(body)
    
    user_db = (
            db_sesion.query(UserModel)
            .filter(UserModel.id == str(event.manager_id.value))
            .first()
        )

    db = mongo["template"]
    user_coll = db["user"]
    user_coll.insert_one(
        {
            "_id": ObjectId(),
            "id": str(event.manager_id.value),
            "first_name": str(event.manager_name.first_name),
            "last_name": str(event.manager_name.last_name),
            "email": str(event.manager_email.value),
            "username": user_db.username,
            "status": "ACTIVE",
            "role": "MANAGER",
            "created_at": event._event_time,
        }
    )