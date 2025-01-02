from common.application.error.application_error import application_error_factory
from inventory.application.errors.codes.inventory_error_codes import InventoryErrorCodes

inventory_not_found_error = application_error_factory(
    code=InventoryErrorCodes.NOT_FOUND.value, message="Product not found"
)
