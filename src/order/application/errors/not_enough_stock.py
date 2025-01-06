from src.order.application.errors.codes.order_error_codes import OrderErrorCodes
from src.common.application.error.application_error import application_error_factory

not_enough_stock_error = application_error_factory(
    code=OrderErrorCodes.NOT_ENOUGH_STOCK.value, message="Not enough stock"
)
