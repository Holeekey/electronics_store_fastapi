from src.common.domain.error.domain_error import domain_error_factory

ORDER_IS_NOT_COMPLETABLE_ERROR = "order_is_not_completable"

order_is_not_completable_error = domain_error_factory(
    ORDER_IS_NOT_COMPLETABLE_ERROR, "Cancelled orders can't be completed"
)
