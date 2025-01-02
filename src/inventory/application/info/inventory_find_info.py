from common.domain.result.result import result_info_factory
from inventory.application.info.codes.inventory_codes import InventoryCodes


inventory_found_info = result_info_factory(
    code=InventoryCodes.FIND_ONE, message="Product found successfully"
)
