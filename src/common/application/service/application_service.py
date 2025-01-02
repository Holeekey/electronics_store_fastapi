from abc import ABCMeta, abstractmethod
from typing import TypeVar

from src.common.domain.result.result import Result

T = TypeVar("T")
U = TypeVar("R")


class IApplicationService(metaclass=ABCMeta):
    @abstractmethod
    async def execute(self, data: T) -> Result[U]:
        pass
