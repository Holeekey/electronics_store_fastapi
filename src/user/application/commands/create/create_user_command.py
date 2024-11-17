from common.application.id_generator.id_generator import IDGenerator
from common.domain.result.result import Result
from common.application.service.application_service import IApplicationService
from user.application.commands.create.types.dto import CreateUserDto
from user.application.commands.create.types.response import CreateUserResponse
from user.application.repositories.user_repository import IUserRepository
from user.application.info.user_created_info import user_created_info
from user.application.models.user import User
from user.application.errors.username_already_exists import username_already_exists_error
from user.application.errors.email_already_exists import email_already_exists_error


class CreateUserCommand(IApplicationService):

    def __init__(self, id_generator: IDGenerator, user_repository: IUserRepository):
        self._user_repository = user_repository
        self._id_generator = id_generator

    async def execute(self, data: CreateUserDto) -> Result[CreateUserResponse]:

        if await self._user_repository.find_by_username(username=data.username):
            return Result.failure(error=username_already_exists_error())
        
        if await self._user_repository.find_by_email(email=data.email):
            return Result.failure(error=email_already_exists_error())

        user = User(
            id=self._id_generator.generate(),
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password=data.password,
            username=data.username,
        )

        await self._user_repository.save(user=user)

        return Result.success(
            value=CreateUserResponse(id=user.id),
            info=user_created_info()
        )
