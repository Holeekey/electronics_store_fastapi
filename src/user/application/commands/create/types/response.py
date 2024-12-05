class CreateUserResponse:
    def __init__(self, id: str):
        self.user_id = id
        
    def __str__(self) -> str:
        return f"id: {self.user_id}"
