from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from common.domain.result.result import Result


T = TypeVar("T", bound=object)


class ITokenProvider(Generic[T], metaclass=ABCMeta):

    @abstractmethod
    def generate(self, data: T) -> Result[str]:
        pass

    def verify(self, token: str) -> Result[T]:
        pass
