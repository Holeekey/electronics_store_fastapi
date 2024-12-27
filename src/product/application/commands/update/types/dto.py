class UpdateProductDto:
    def __init__(self, id:str, code:str, name: str, description:str, cost: float, margin:float):
        self.id = id
        self.code = code
        self.name = name
        self.description = description
        self.cost = cost
        self.margin = margin
