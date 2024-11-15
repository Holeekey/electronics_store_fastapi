from typing import Callable, TypeVar
from common.application.error.application_error import ApplicationError
from common.application.result.application_result import AppResult, ResultInfo
from common.application.service.application_service import IApplicationService

T = TypeVar("T")
R = TypeVar("R")

class ErrorDecorator(IApplicationService):
    def __init__(self, service: IApplicationService, error_handler: Callable[[ApplicationError], Exception]):
        self._service = service
        self._error_handler = error_handler

    async def execute(self, data: T) -> AppResult[R]:
        result = await self._service.execute(data)
        if(result.is_error()):
            raise result.handleError(self._error_handler)
        return result