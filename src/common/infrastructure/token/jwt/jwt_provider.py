from datetime import datetime, timedelta, timezone
from typing import Dict, Generic, TypeVar
from common.application.token.errors import invalid_token_error
from common.application.token.info.token_created_info import token_created_info
from common.application.token.info.token_verified_info import token_verified_info
from common.application.token.token_provider import ITokenProvider
from common.domain.result.result import Result
from config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, TOKEN_ALGORITHM
from jose import jwt

T = TypeVar("T", bound=Dict[str, str])

class JwtProvider(Generic[T],ITokenProvider[T]):
    
    def create(self, data: dict) -> Result[str]:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, TOKEN_ALGORITHM)
        
        return Result.success(encoded_jwt, token_created_info())
    
    def verify(self, token: str) -> Result[T]:
        payload = jwt.decode(token, SECRET_KEY, TOKEN_ALGORITHM)
        for key in T:
            if key not in payload:
                return Result.failure(invalid_token_error())
        return Result.success(payload, token_verified_info())