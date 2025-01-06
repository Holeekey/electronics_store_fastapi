from src.common.domain.result.result import result_info_factory
from src.product.application.info.codes.product_codes import ProductCodes


product_updated_info = result_info_factory(
    code=ProductCodes.UPDATE.value, message="Product has been updated successfully"
)
