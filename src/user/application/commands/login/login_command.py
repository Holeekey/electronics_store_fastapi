from common.application.service.application_service import IApplicationService
from common.application.token.token_provider import ITokenProvider
from common.domain.result.result import Result
from user.application.commands.login.types.login_dto import LoginDto
from user.application.commands.login.types.login_response import LoginResponse
from user.application.errors.invalid_credentials import invalid_credentials_error
from user.application.info.user_logged_in_info import user_logged_in_info
from user.application.repositories.user_repository import IUserRepository


class LoginCommand(IApplicationService):
    def __init__(self, user_repository: IUserRepository, token_provider: ITokenProvider):
        self.user_repository = user_repository
        self.token_provider = token_provider

    async def execute(self, data: LoginDto) -> Result[LoginResponse]:
        
        user = await self.user_repository.find_by_login_credential(data.login_credential)

        if user is None:
            return Result.failure(invalid_credentials_error())

        if user.password != data.password:
            return Result.failure(invalid_credentials_error())

        token_result = self.token_provider.generate(dict(id=user.id))

        return Result.success(LoginResponse(token=token_result.unwrap()), info=user_logged_in_info())
    