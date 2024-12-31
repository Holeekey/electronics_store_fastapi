from bson import ObjectId
import jsonpickle

from src.common.infrastructure.database.database import get_session
from src.common.infrastructure.database.mongo import get_mongo_client
from src.user.infrastructure.models.postgres.sqlalchemy.user_model import UserModel

def client_created_projector(ch, method, properties, body):
    
    mongo = get_mongo_client().__next__()
    db_sesion = get_session().__next__()
    
    event = jsonpickle.decode(body)
    
    user_db = (
            db_sesion.query(UserModel)
            .filter(UserModel.id == str(event.client_id.value))
            .first()
        )

    db = mongo["template"]
    user_coll = db["user"]
    user_coll.insert_one(
        {
            "_id": ObjectId(),
            "id": str(event.client_id.value),
            "first_name": str(event.client_name.first_name),
            "last_name": str(event.client_name.last_name),
            "email": str(event.client_email.value),
            "username": user_db.username,
            "status": "ACTIVE",
            "role": "CLIENT",
            "created_at": event._event_time,
        }
    )