from src.common.domain.error.domain_error import domain_error_factory

INVALID_INVENTORY_STOCK_ERROR = "invalid_inventory_stock"

invalid_inventory_stock_error = domain_error_factory(
    INVALID_INVENTORY_STOCK_ERROR, "Invalid inventory stock"
)
