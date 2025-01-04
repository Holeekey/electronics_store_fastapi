from enum import Enum


class ShoppingCartErrorCodes(Enum):
    CLIENT_NOT_FOUND = "SC-E-001"
    PRODUCT_NOT_FOUND = "SC-E-002"
    CLIENT_SHOPPING_CART_DOES_NOT_INCLUDES_PRODUCT = "SC-E-003"
