from common.application.error.application_error import application_error_factory
from inventory.application.errors.codes.inventory_error_codes import InventoryErrorCodes

negative_stock = application_error_factory(
    code=InventoryErrorCodes.STOCK_NEGATIVE.value, message="Stock cannot be negative"
)
