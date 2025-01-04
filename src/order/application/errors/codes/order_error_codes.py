from enum import Enum


class OrderErrorCodes(Enum):
    CLIENT_NOT_FOUND = "OR-E-001"
    SHOPPING_CART_EMPTY = "OR-E-002"
