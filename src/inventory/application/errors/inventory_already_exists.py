from common.application.error.application_error import application_error_factory
from inventory.application.errors.codes.inventory_error_codes import InventoryErrorCodes

inventory_already_exists_error = application_error_factory(
    code=InventoryErrorCodes.USERNAME_ALREADY_EXISTS.value, message="Inventory already used"
)
