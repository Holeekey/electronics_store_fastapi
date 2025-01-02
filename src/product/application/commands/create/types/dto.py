class CreateProductDto:
    def __init__(self, code:str, name: str, description:str, cost: float, margin:float):
        self.code = code
        self.name = name
        self.description = description
        self.cost = cost
        self.margin = margin
