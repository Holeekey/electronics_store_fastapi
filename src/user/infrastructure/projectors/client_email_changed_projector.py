import jsonpickle
from common.infrastructure.database.database import get_session
from common.infrastructure.database.mongo import get_mongo_client
from user.infrastructure.models.postgres.sqlalchemy.user_model import UserModel


def client_email_changed_projector(ch, method, properties, body):
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
    
    filter = {"id": str(event.client_id.value)}
    
    update = {
        "$set": {
            "email": str(event.client_email.value),
            "username": user_db.username,
        }
    }
    
    user_coll.update_one(filter, update, upsert=True)