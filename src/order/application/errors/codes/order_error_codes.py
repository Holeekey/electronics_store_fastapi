from enum import Enum


class OrderErrorCodes(Enum):
    CLIENT_NOT_FOUND = "OR-E-001"
    SHOPPING_CART_EMPTY = "OR-E-002"
    ORDER_IS_NOT_COMPLETABLE = "OR-E-003"
    ORDER_IS_NOT_CANCELABLE = "OR-E-004"
    NOT_ENOUGH_STOCK = "OR-E-005"
    NOT_FOUND = "OR-E-NF"
