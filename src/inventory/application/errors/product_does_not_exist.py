from src.common.application.error.application_error import application_error_factory
from src.inventory.application.errors.codes.inventory_error_codes import InventoryErrorCodes

product_does_not_exist = application_error_factory(
    code=InventoryErrorCodes.PRODUCT_DOES_NOT_EXIST.value, message="Product does not exist"
)