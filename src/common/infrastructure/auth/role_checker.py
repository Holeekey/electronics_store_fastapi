from typing import Annotated, List

from fastapi import Depends, HTTPException, status

from src.common.infrastructure.auth.get_current_user import get_current_user
from src.common.infrastructure.auth.models.auth_user import AuthUser, AuthUserRole


def role_checker(allowed_roles: List[AuthUserRole]):
    def function(user: Annotated[AuthUser, Depends(get_current_user)]):
        if user.role.name in [role.name for role in allowed_roles]:
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have enough permissions",
        )

    return function
