from src.common.domain.events.domain_event import DomainEvent
from src.product.domain.value_objects.product_id import ProductId
from src.product.domain.value_objects.product_name import ProductName
from src.product.domain.value_objects.product_pricing import ProductPricing
from src.product.domain.value_objects.product_code import ProductCode
from src.product.domain.value_objects.product_description import ProductDescription

PRODUCT_CREATED = "product_created"


class ProductCreated(DomainEvent):
    def __init__(self, product_id: ProductId, code: ProductCode, name: ProductName, description: ProductDescription, pricing: ProductPricing):
        super().__init__(PRODUCT_CREATED)
        self.product_id = product_id
        self.product_code = code
        self.product_name = name
        self.product_description = description
        self.product_pricing = pricing
