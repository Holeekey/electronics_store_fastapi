from src.order.application.errors.codes.order_error_codes import OrderErrorCodes
from src.common.application.error.application_error import application_error_factory

order_not_completable_error = application_error_factory(
    code=OrderErrorCodes.ORDER_IS_NOT_COMPLETABLE.value, message="Cancelled orders are not completable"
)
