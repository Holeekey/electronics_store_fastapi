import pytest


from src.product.application.commands.create.types.dto import CreateProductDto

def product_payload(code= "TEST-00", name= "TestProduct", description= "Test Description", cost= 1.0, margin= 0.5) -> CreateProductDto:
  return CreateProductDto(
    code= code,
    name= name,
    description= description,
    cost= cost,
    margin= margin
  )