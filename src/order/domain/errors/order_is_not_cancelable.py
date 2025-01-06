from src.common.domain.error.domain_error import domain_error_factory

ORDER_IS_NOT_CANCELABLE_ERROR = "order_is_not_cancelable"

order_is_not_cancelable_error = domain_error_factory(
    ORDER_IS_NOT_CANCELABLE_ERROR, "Completed orders can't be cancelled"
)
