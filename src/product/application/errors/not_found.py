from src.common.application.error.application_error import application_error_factory
from src.product.application.errors.codes.product_error_codes import ProductErrorCodes

product_not_found_error = application_error_factory(
    code=ProductErrorCodes.NOT_FOUND.value, message="Product not found"
)
