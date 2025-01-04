from src.common.application.error.application_error import application_error_factory
from src.product.application.errors.codes.product_error_codes import ProductErrorCodes

product_name_already_exists_error = application_error_factory(
    code=ProductErrorCodes.NAME_ALREADY_EXISTS.value,
    message="Product name already exists",
)
