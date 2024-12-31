from typing import Generic, TypeVar

from src.common.infrastructure.responses.info import ResponseInfo


T = TypeVar("T")


class Response(Generic[T]):
    def __init__(self, info: ResponseInfo, response: T = None):
        self._info = info
        self._response = response

    def to_dict(self):
        return {"info": self._info.to_dict(), "response": self._response}
