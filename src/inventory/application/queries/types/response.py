class FindOneInventoryResponse:
    def __init__(self, product_id: str, product_name:str, stock: int):
        self.product_id = product_id
        self.product_name = product_name
        self.stock = stock
