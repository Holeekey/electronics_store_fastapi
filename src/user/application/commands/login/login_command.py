from src.common.application.cryptography.cryptography_provider import ICryptographyProvider
from src.common.application.service.application_service import IApplicationService
from src.common.application.token.token_provider import ITokenProvider
from src.common.domain.result.result import Result
from src.user.application.commands.login.types.login_dto import LoginDto
from src.user.application.commands.login.types.login_response import LoginResponse
from src.user.application.errors.invalid_credentials import invalid_credentials_error
from src.user.application.errors.suspended import user_suspended_error
from src.user.application.info.user_logged_in_info import user_logged_in_info
from src.user.application.repositories.user_repository import IUserRepository
from src.user.application.models.user import UserStatus


class LoginCommand(IApplicationService):
    def __init__(
        self, user_repository: IUserRepository, token_provider: ITokenProvider, cryptography_provider: ICryptographyProvider[str, str]
    ):
        self.user_repository = user_repository
        self.token_provider = token_provider
        self.cryptography_provider = cryptography_provider

    async def execute(self, data: LoginDto) -> Result[LoginResponse]:

        user = await self.user_repository.find_by_login_credential(
            data.login_credential
        )

        if user is None:
            return Result.failure(invalid_credentials_error())

        if self.cryptography_provider.decrypt(user.password) != data.password:
            return Result.failure(invalid_credentials_error())

        if user.status.value == UserStatus.SUSPENDED.value:
            return Result.failure(user_suspended_error())

        token_result = self.token_provider.generate(dict(id=user.id))

        return Result.success(
            LoginResponse(token=token_result.unwrap()), info=user_logged_in_info()
        )
