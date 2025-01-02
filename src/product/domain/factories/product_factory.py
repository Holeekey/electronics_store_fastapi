from product.domain.product import Product
from product.domain.value_objects.product_id import ProductId
from product.domain.value_objects.product_code import ProductCode
from product.domain.value_objects.product_name import ProductName
from product.domain.value_objects.product_description import ProductDescription
from product.domain.value_objects.product_pricing import ProductPricing
from product.domain.value_objects.product_status import ProductStatus, ProductStatusOptions


def product_factory(id: str, code:str, name: str, description:str, cost: float, margin:float, status:int):

    product_id = ProductId(id)
    product_code = ProductCode(code)
    product_name = ProductName(name)
    product_description = ProductDescription(description)
    product_pricing = ProductPricing(cost, margin)
    product_status: ProductStatus = None #! Should this directly raise an error?
    if (status == 0):
        product_status = ProductStatus(ProductStatusOptions.INACTIVE)
    elif (status == 1):
        product_status = ProductStatus(ProductStatusOptions.ACTIVE)

    return Product(product_id, product_code, product_name, product_description, product_pricing, product_status)
