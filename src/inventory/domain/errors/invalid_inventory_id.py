from src.common.domain.error.domain_error import domain_error_factory

INVALID_INVENTORY_ID_ERROR = "invalid_inventory_id"

invalid_inventory_id_error = domain_error_factory(
    INVALID_INVENTORY_ID_ERROR, "Invalid inventory ID"
)
