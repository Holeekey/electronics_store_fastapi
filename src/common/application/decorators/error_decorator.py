from typing import Callable, TypeVar
from src.common.application.error.application_error import ApplicationError
from src.common.application.service.application_service import IApplicationService
from src.common.domain.result.result import Result

T = TypeVar("T")
R = TypeVar("R")


class ErrorDecorator(IApplicationService):
    def __init__(
        self,
        service: IApplicationService,
        error_handler: Callable[[ApplicationError], Exception],
    ):
        self._service = service
        self._error_handler = error_handler

    async def execute(self, data: T) -> Result[R]:
        result = await self._service.execute(data)
        if result.is_error():
            raise result.handle_error(self._error_handler)
        return result
