from datetime import datetime, timedelta, timezone
from typing import Dict, Generic, List, TypeVar
from src.common.application.token.errors.invalid_token_error import invalid_token_error
from src.common.application.token.info.token_created_info import token_created_info
from src.common.application.token.info.token_verified_info import token_verified_info
from src.common.application.token.token_provider import ITokenProvider
from src.common.domain.result.result import Result
from src.common.infrastructure.auth.payload.token_payload import TokenPayload
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, TOKEN_ALGORITHM
from jose import JWTError, jwt

T = TypeVar("T")


class JwtProvider(Generic[T], ITokenProvider[T]):

    def __init__(self, keys: List[str]):
        self.keys = keys

    def generate(self, data: dict) -> Result[str]:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, TOKEN_ALGORITHM)

        return Result.success(encoded_jwt, token_created_info())

    def verify(self, token: str) -> Result[T]:
        try:
            payload = jwt.decode(token, SECRET_KEY, TOKEN_ALGORITHM)
            for key in self.keys:
                if key not in payload:
                    return Result.failure(invalid_token_error())
            return Result.success(payload, token_verified_info())
        except JWTError as e:
            return Result.failure(invalid_token_error())


def get_jwt_provider():
    jwt_provider = JwtProvider[TokenPayload](keys=TokenPayload.__annotations__.keys())
    return jwt_provider
