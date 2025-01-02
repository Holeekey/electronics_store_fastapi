from src.common.domain.result.result import result_info_factory
from src.product.application.info.codes.product_codes import ProductCodes


product_found_info = result_info_factory(
    code=ProductCodes.FIND_ONE, message="Product found successfully"
)
