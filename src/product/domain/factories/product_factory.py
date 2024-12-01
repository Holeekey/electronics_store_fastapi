from product.domain.product import Product
from product.domain.value_objects.product_id import ProductId
from product.domain.value_objects.product_name import ProductName
from product.domain.value_objects.product_price import ProductPrice
from product.domain.value_objects.product_status import ProductStatus, ProductStatusOptions


def product_factory(id: str, name: str, price: str, status:int):

    product_id = ProductId(id)
    product_name = ProductName(name)
    product_price = ProductPrice(price)
    product_status: ProductStatus = None #! Should this directly raise an error?
    if (status == 0):
        product_status = ProductStatus(ProductStatusOptions.INACTIVE)
    elif (status == 1):
        product_status = ProductStatus(ProductStatusOptions.ACTIVE)

    return Product(product_id, product_name, product_price, product_status)
