import math
from typing import Generic, TypeVar

from common.infrastructure.responses.info import ResponseInfo


T = TypeVar("T")

class PaginationInfo:
    def __init__(
        self,
        page: int,
        per_page: int,
        count: int,
        pages: int,
        prev: int | None,
        next: int | None,
    ):
        self._page = page
        self._per_page = per_page
        self._count = count
        self._pages = pages
        self._prev = prev
        self._next = next
    
    def to_dict(self):
        return {
            "page": self._page,
            "per_page": self._per_page,
            "pages": self._pages,
            "count": self._count,
            "prev": self._prev,
            "next": self._next
        }
        
        
    @staticmethod
    def make_pagination_info(page, per_page, count):
        pages = math.ceil(count / per_page)
        prev_page = page - 1 if page > 1 else None 
        next_page = page + 1 if page < pages else None 
        
        return PaginationInfo(
            page=page,
            per_page=per_page,
            count=count,
            pages=pages,
            prev=prev_page,
            next=next_page,
        )
         

class PaginationResponse(Generic[T]):
    def __init__(self, info: ResponseInfo, pagination_info: PaginationInfo, response: T = None):
        self._info = info
        self._pagination = pagination_info
        self._response = response

    def to_dict(self):
        return {
            "info": self._info.to_dict(),
            "pagination": self._pagination.to_dict(),
            "response": self._response
        }
