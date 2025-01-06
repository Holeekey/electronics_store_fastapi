from src.common.domain.error.domain_error import domain_error_factory

PRODUCT_ALREADY_DELETED_ERROR = "product_already_deleted"

product_already_deleted_error = domain_error_factory(
    PRODUCT_ALREADY_DELETED_ERROR, "Product is already inactive. Cannot be deactivated again"
)