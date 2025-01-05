from src.order.application.errors.codes.order_error_codes import OrderErrorCodes
from src.common.application.error.application_error import application_error_factory

order_not_found_error = application_error_factory(
    code=OrderErrorCodes.NOT_FOUND.value, message="Order not found"
)
