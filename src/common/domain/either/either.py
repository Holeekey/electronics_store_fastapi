from typing import Generic, Optional, TypeVar

from src.common.domain.utils import is_not_none

L = TypeVar("L")
R = TypeVar("R")


class Either(Generic[L, R]):

    def __init__(self, left: Optional[L] = None, right: Optional[R] = None):
        self.left = left
        self.right = right

    def is_left(self) -> bool:
        return is_not_none(self.left)

    def is_right(self) -> bool:
        return is_not_none(self.right)

    def get_left(self) -> L:
        if self.is_right():
            raise ValueError("Either is right")
        return self.left

    def get_right(self) -> R:
        if self.is_left():
            raise ValueError("Either is left")
        return self.right

    @staticmethod
    def make_left(left: L) -> "Either[L,R]":
        return Either(left=left, right=None)

    @staticmethod
    def make_right(right: R) -> "Either[L,R]":
        return Either(left=None, right=right)
