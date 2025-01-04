from typing import Dict
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.common.domain.utils.is_none import is_none
from src.common.infrastructure.auth.models.auth_user import AuthUserRole, AuthUserStatus
from src.common.infrastructure.auth.payload.token_payload import TokenPayload
from src.common.infrastructure.auth.repositories.postgres.sqlalchemy.auth_user_repository import (
    AuthUserRepositorySqlAlchemy,
)
from src.common.infrastructure.database.database import get_session
from src.common.infrastructure.token.jwt.jwt_provider import JwtProvider
from src.config import API_PREFIX
from src.user.application.queries.find_one.find_one_user_query import FindOneUserQuery
from src.user.application.queries.find_one.types.dto import FindOneUserDto
from src.user.application.queries.find_one.types.response import FindOneUserResponse
from src.user.infrastructure.repositories.postgres.sqlalchemy.user_repository import (
    UserRepositorySqlAlchemy,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PREFIX}/user/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)
):

    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    suspend_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User is suspended, talk to the admin",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_verifier = JwtProvider[TokenPayload](keys=TokenPayload.__annotations__.keys())

    verifyResult = token_verifier.verify(token)

    if verifyResult.is_error():
        raise auth_exception

    auth_user_repo = AuthUserRepositorySqlAlchemy(db)

    user = auth_user_repo.get_user_by_id(verifyResult.unwrap()["id"])

    if is_none(user):
        raise auth_exception

    if user.status.value == AuthUserStatus.SUSPENDED.value:
        raise suspend_exception

    return user
