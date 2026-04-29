from typing import Annotated, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import ResponseMessage
from app.core.db import get_async_session
from app.core.enums import Role
from app.core.security import decode_access_token
from app.crud.user import user_crud
from app.models.user import User

security = HTTPBearer(auto_error=False)
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


async def get_current_user(
    session: SessionDep,
    token: Annotated[
        HTTPAuthorizationCredentials | None, Depends(security)
    ] = None,
) -> User | None:
    """Базовая зависимость: извлекает пользователя по токену без исключений."""
    if not token:
        return None

    token_string = token.credentials

    user_id = decode_access_token(token_string)
    if not user_id:
        return None

    user = await user_crud.get(session, user_id)
    if not user or not user.is_active:
        return None

    return user


def role_required(allowed_role: Role) -> Callable:
    """Фабрика для проверки конкретной роли."""

    async def check_role(
        user: User | None = Depends(get_current_user),
    ) -> User:
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ResponseMessage.error_401,
            )
        if user.role != allowed_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ResponseMessage.error_403,
            )
        return user

    # Для уникальности имени функции (чтобы FastAPI не путал зависимости)
    check_role.__name__ = f'role_required_{allowed_role.value}'
    return check_role


async def current_user_required(
    user: User | None = Depends(get_current_user),
) -> User:
    """Только авторизованный пользователь (любая роль)."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ResponseMessage.error_401,
        )
    return user


get_current_user_authorizer = current_user_required
get_admin_authorizer = role_required(Role.ADMIN)

CurrentUser = Annotated[User, Depends(current_user_required)]
AdminUser = Annotated[User, Depends(role_required(Role.ADMIN))]
