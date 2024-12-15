
from bson import ObjectId
from diator.events import EventHandler

from common.infrastructure.database.database import DbSession
from common.infrastructure.database.mongo import MongoSession
from user.infrastructure.events.user_created.manager_created import ManagerCreatedDiator
from user.infrastructure.models.postgres.sqlalchemy.user_model import UserModel

class ManagerCreatedProjector(EventHandler[ManagerCreatedDiator]):
    def __init__(self, mongo_session: MongoSession, db_session: DbSession) -> None:
        self._mongo = mongo_session
        self._db = db_session.session
        
        
    async def handle(self, event: ManagerCreatedDiator) -> None:
        user_db = self._db.query(UserModel).filter(UserModel.id == str(event.manager_id)).first()
        
        print(id(self._mongo))
        
        session = self._mongo.session
        db = session["template"]
        user_coll = db["user"]
        
        user_coll.insert_one({
            "_id": ObjectId(),
            "id": str(event.manager_id),
            "first_name": str(event.manager_first_name),
            "last_name": str(event.manager_last_name),
            "email": str(event.manager_email),
            "username": user_db.username,
            "status": "ACTIVE",
            "role": "MANAGER",
            "created_at": event.timestamp
        })