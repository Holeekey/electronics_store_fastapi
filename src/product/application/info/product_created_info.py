from src.common.domain.result.result import result_info_factory
from src.product.application.info.codes.product_codes import ProductCodes


product_created_info = result_info_factory(
    code=ProductCodes.CREATE.value, message="Product created successfully"
)
