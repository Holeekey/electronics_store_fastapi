from enum import Enum


class InventoryErrorCodes(Enum):
    INVENTORY_ALREADY_EXISTS = "INV-E-001"
    STOCK_NEGATIVE = "INV-E-002"
    PRODUCT_DOES_NOT_EXIST = "INV-E-003"
    NOT_FOUND = "INV-E-NF"
