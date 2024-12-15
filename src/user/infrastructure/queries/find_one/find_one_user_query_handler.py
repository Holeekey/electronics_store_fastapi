
from diator.requests import RequestHandler
from diator.events import Event

from common.domain.utils.is_none import is_none
from common.infrastructure.database.mongo import MongoSession
from common.infrastructure.loggers.loguru_logger import LoguruLogger
from common.infrastructure.responses.handlers.error_response_handler import error_response_handler
from common.infrastructure.responses.handlers.success_response_handler import success_response_handler
from user.application.info.user_found_info import user_found_info
from user.infrastructure.queries.find_one.types.query import FindOneUserQuery
from user.infrastructure.queries.find_one.types.response import FindOneUserReponse
from user.application.errors.not_found import user_not_found_error

class FindOneUserQueryHandler(RequestHandler[FindOneUserQuery, FindOneUserReponse]):
    def __init__(self,mongo_session: MongoSession) -> None:
        self._mongo = mongo_session
        self._logger = LoguruLogger('Find One User')
        self._events = []

    @property
    def events(self) -> list[Event]:
        return self._events

    async def handle(self, request: FindOneUserQuery) -> FindOneUserReponse:
        session = self._mongo.session
        db = session["template"]
        user_coll = db["user"]

        user = user_coll.find_one({"id": request.id})
        
        if is_none(user):
            error = user_not_found_error()
            raise error_response_handler(error) 
        
        response = FindOneUserReponse(
            id=user["id"],
            username=user["username"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            role=user["role"],
            status=user["status"]
        )
        
        return success_response_handler(response, user_found_info())