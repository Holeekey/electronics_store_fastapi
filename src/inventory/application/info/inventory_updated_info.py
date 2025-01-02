from common.domain.result.result import result_info_factory
from inventory.application.info.codes.inventory_codes import InventoryCodes


inventory_updated_info = result_info_factory(
    code=InventoryCodes.UPDATE, message="Inventory updated successfully"
)
