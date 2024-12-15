from diator.requests import RequestHandler
from diator.events.event import Event

from common.application.decorators.error_decorator import ErrorDecorator
from common.application.decorators.logger_decorator import LoggerDecorator
from common.infrastructure.cryptography.fernetCryptography_provider import FernetProvider
from common.infrastructure.database.database import DbSession
from common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
from common.infrastructure.loggers.loguru_logger import LoguruLogger
from common.infrastructure.responses.handlers.error_response_handler import error_response_handler
from common.infrastructure.responses.handlers.success_response_handler import success_response_handler
from user.application.commands.create.create_user_command import CreateUserService
from user.infrastructure.repositories.postgres.sqlalchemy.user_repository import UserRepositorySqlAlchemy
from user.application.commands.create.types.response import CreateUserResponse
from user.infrastructure.commands.create_user_command import CreateUserCommand

class CreateUserCommandHandler(RequestHandler[CreateUserCommand, CreateUserResponse]):
    
    def __init__(self,
        session: DbSession,
        fernetProvider: FernetProvider,
        uuid_generator: UUIDGenerator
    ):
        self._db_session = session
        self._cryptography_provider = fernetProvider
        self._uuid_generator = uuid_generator 
        self._events = []   
    
    @property
    def events(self) -> list[Event]:
        return self._events
    
    async def handle(self,
        request: CreateUserCommand,
    ) -> CreateUserResponse:
        result = await ErrorDecorator(
            service= LoggerDecorator(
                service= CreateUserService(
                    user_repository= UserRepositorySqlAlchemy(self._db_session.session),
                    id_generator= self._uuid_generator,
                    cryptography_provider= self._cryptography_provider
                ),
                loggers = [LoguruLogger("Create User")]
            ),
            error_handler=error_response_handler,
        ).execute(data=request)

        return result.handle_success(handler=success_response_handler)