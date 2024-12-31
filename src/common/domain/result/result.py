from typing import Callable, Generic, TypeVar, Optional

from src.common.application.error.application_error import ApplicationError
from src.common.domain.utils.is_none import is_none
from src.common.domain.utils.is_not_none import is_not_none
from src.common.domain.error.error import Error

T = TypeVar("T")
R = TypeVar("R")


class ResultInfo:
    def __init__(self, code: str, message: str, data=None):
        self._code = code
        self._message = message
        self._data = data

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message

    @property
    def data(self):
        return self._data

    def to_dict(self):
        return {
            "code": self._code,
            "message": self._message,
            "data": self._data.__str__() if is_not_none(self._data) else None,
        }


def result_info_factory(code: str, message: str):
    def func(info=None):
        return ResultInfo(code=code, message=message, data=info)

    return func


class Result(Generic[T]):
    def __init__(
        self,
        value: Optional[T] = None,
        error: Optional[Error] = None,
        info: Optional[ResultInfo] = None,
    ) -> None:
        if is_none(value) and is_none(error):
            raise ValueError("Value and error cannot be both None")
        if is_not_none(value) and is_not_none(error):
            raise ValueError("Value and error cannot be both not None")
        if is_not_none(value) and is_none(info):
            raise ValueError("Info cannot be None if value is not None")
        self._value = value
        self._error = error
        self._info = info

    def is_success(self) -> bool:
        return is_not_none(self._value)

    def is_error(self) -> bool:
        return is_not_none(self._error)

    def unwrap(self) -> T:
        if is_not_none(self._value):
            return self._value
        raise self._error

    def unwrap_or_default(self, default: T) -> T:
        if is_not_none(self._value):
            return self._value
        return default

    def handle_error(self, handler: Callable[[Error], R]):
        if is_none(self._error):
            raise Exception("Cannot handle error")
        return handler(self._error)

    def handle_success(self, handler: Callable[[T, ResultInfo], R]):
        if is_none(self._value):
            raise Exception("Cannot handle without value")
        return handler(self._value, self._info)

    @staticmethod
    def success(value: T, info: ResultInfo) -> "Result[T]":
        return Result(value=value, info=info)

    @staticmethod
    def failure(error: Exception) -> "Result[T]":
        return Result(error=error)
