from common.domain.events.domain_event import DomainEvent
from product.domain.value_objects.product_id import ProductId
from product.domain.value_objects.product_name import ProductName
from product.domain.value_objects.product_pricing import ProductPricing

PRODUCT_CREATED = "product_created"


class ProductCreated(DomainEvent):
    def __init__(self, product_id: ProductId, name: ProductName, price: ProductPricing):
        super().__init__(PRODUCT_CREATED)
        self.product_id = product_id
        self.product_name = name
        self.product_price = price
