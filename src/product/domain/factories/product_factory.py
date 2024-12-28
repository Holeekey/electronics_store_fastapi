from product.domain.product import Product
from product.domain.value_objects.product_id import ProductId
from product.domain.value_objects.product_name import ProductName
from product.domain.value_objects.product_price import ProductPrice


def product_factory(id: str, name: str, price: str):

    product_id = ProductId(id)
    product_name = ProductName(name)
    product_price = ProductPrice(price)

    return Product(product_id, product_name, product_price)
