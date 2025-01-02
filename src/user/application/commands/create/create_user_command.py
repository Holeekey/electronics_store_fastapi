from src.common.application.cryptography.cryptography_provider import ICryptographyProvider
from src.common.application.events.event_handlers import IEventPublisher
from src.common.application.id_generator.id_generator import IDGenerator
from src.common.domain.result.result import Result
from src.common.application.service.application_service import IApplicationService
from src.common.domain.utils.is_not_none import is_not_none
from src.user.application.commands.create.types.dto import CreateUserDto
from src.user.application.commands.create.types.response import CreateUserResponse
from src.user.application.repositories.user_repository import IUserRepository
from src.user.application.info.user_created_info import user_created_info
from src.user.application.models.user import User, UserRole, UserStatus
from src.user.application.errors.username_already_exists import (
    username_already_exists_error,
)
from src.user.application.errors.email_already_exists import email_already_exists_error
from src.user.domain.client.factories.client_factory import client_factory
from src.user.domain.manager.factories.manager_factory import manager_factory


class CreateUserCommand(IApplicationService):

    def __init__(
        self,
        id_generator: IDGenerator,
        user_repository: IUserRepository,
        cryptography_provider: ICryptographyProvider[str, str],
        event_publisher: IEventPublisher,
    ):
        self._user_repository = user_repository
        self._id_generator = id_generator
        self._cryptography_provider = cryptography_provider
        self._event_publisher = event_publisher

    async def execute(self, data: CreateUserDto) -> Result[CreateUserResponse]:
        if await self._user_repository.find_by_username(username=data.username):
            return Result.failure(error=username_already_exists_error())

        if await self._user_repository.find_by_email(email=data.email):
            return Result.failure(error=email_already_exists_error())

        client = None
        manager = None

        id = self._id_generator.generate()

        if data.role.name == UserRole.CLIENT.name:
            client = client_factory(
                id=id,
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
            )

        if data.role.name == UserRole.MANAGER.name:
            manager = manager_factory(
                id=id,
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
            )

        user = User(
            id=id,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password= self._cryptography_provider.encrypt(data.password),
            username=data.username,
            role=data.role,
            status=UserStatus.ACTIVE,
        )

        await self._user_repository.save(user=user)

        if is_not_none(client):
            await self._event_publisher.publish(client.pull_events())
            
        if is_not_none(manager):
            await self._event_publisher.publish(manager.pull_events())

        return Result.success(
            value=CreateUserResponse(id=user.id), info=user_created_info()
        )
