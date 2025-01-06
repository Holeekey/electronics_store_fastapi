from src.common.domain.result.result import result_info_factory
from src.product.application.info.codes.product_codes import ProductCodes


product_deleted_info = result_info_factory(
    code=ProductCodes.DELETE.value, message="Product has been deactivated successfully"
)
