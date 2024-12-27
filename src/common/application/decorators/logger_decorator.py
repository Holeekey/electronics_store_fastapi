import json
from typing import List, TypeVar
from common.application.error.application_error import ApplicationError
from common.application.logger.logger import ILogger
from common.application.service.application_service import IApplicationService
from common.domain.result.result import Result

T = TypeVar("T")
R = TypeVar("R")


class LoggerDecorator(IApplicationService):
    def __init__(
        self,
        service: IApplicationService,
        loggers: List[ILogger],
    ):
        self._service = service
        self._loggers = loggers

    async def execute(self, data: T) -> Result[R]:
        
        try:
            for logger in self._loggers:
                log = data.to_dict() if hasattr(data, 'to_dict') else json.dumps(vars(data), default=str)
                logger.log(f"INPUT", log)
            result = await self._service.execute(data)
            
            if result.is_error():
                for logger in self._loggers:
                    logger.error(result.handle_error(lambda e: e))
            else:
                for logger in self._loggers:
                    log = data.to_dict() if hasattr(result.unwrap(), 'to_dict') else json.dumps(vars(result.unwrap()), default=str)
                    logger.log(f"RESULT", log)
            
            return result
            
        except ValueError as e:
            for logger in self._loggers:
                logger.exception(e.__str__())
                raise e
        
        
        
