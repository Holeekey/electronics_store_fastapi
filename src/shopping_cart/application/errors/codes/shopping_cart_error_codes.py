from enum import Enum


class ShoppingCartErrorCodes(Enum):
    CLIENT_NOT_FOUND = "SC-E-001"
    PRODUCT_NOT_FOUND = "SC-E-002"
