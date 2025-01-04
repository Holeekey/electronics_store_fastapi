from pydantic import BaseModel


class LoginDto(BaseModel):
    login_credential: str
    password: str
