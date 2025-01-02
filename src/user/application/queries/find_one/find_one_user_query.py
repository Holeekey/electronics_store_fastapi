from src.common.domain.result.result import Result
from src.common.application.service.application_service import IApplicationService
from src.common.domain.utils.is_none import is_none
from src.user.application.info.user_found_info import user_found_info
from src.user.application.queries.find_one.types.response import FindOneUserResponse
from src.user.application.repositories.user_repository import IUserRepository
from src.user.application.queries.find_one.types.dto import FindOneUserDto
from src.user.application.errors.not_found import user_not_found_error


class FindOneUserQuery(IApplicationService):

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, data: FindOneUserDto) -> Result[FindOneUserResponse]:

        user = await self.user_repository.find_one(data.id)

        if is_none(user):
            return Result.failure(error=user_not_found_error())

        return Result.success(
            FindOneUserResponse(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                role=user.role,
                status=user.status,
            ),
            info=user_found_info(),
        )
