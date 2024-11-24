from pydantic import BaseModel


class TokenPayload(BaseModel):
    id: str
    