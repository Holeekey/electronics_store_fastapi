from src.common.domain.result.result import result_info_factory
from src.inventory.application.info.codes.inventory_codes import InventoryCodes


inventory_created_info = result_info_factory(
    code=InventoryCodes.CREATE, message="Inventory created successfully"
)
