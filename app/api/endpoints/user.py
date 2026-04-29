from typing import Sequence

from fastapi import APIRouter, Query, status

from app.api.deps import AdminUser, CurrentUser, SessionDep
from app.api.responses import ResponsesSettings
from app.core.constants import UserConstants
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate, UserUpdateAdmin
from app.services.user import user_service

router = APIRouter()
admin_updater_router = APIRouter()


@router.get(
    '/me',
    response_model=UserRead,
    responses=ResponsesSettings.ERROR_401,
    summary=UserConstants.GET_ME_SUM,
)
async def get_me(user: CurrentUser) -> User:
    """Возвращает профиль текущего авторизованного пользователя.

    Только авторизированные.
    """
    return await user_service.get_my_profile(user)


@router.patch(
    '/me',
    response_model=UserRead,
    responses={**ResponsesSettings.ERROR_401, **ResponsesSettings.ERROR_422},
    summary=UserConstants.PATCH_ME_SUM,
)
async def update_me(
    obj_in: UserUpdate, session: SessionDep, user: CurrentUser
) -> User:
    """Обновляет данные профиля текущего пользователя.

    Доступно всем.
    """
    return await user_service.update_profile(session, user, obj_in)


@admin_updater_router.patch(
    '',
    response_model=UserRead,
    responses={**ResponsesSettings.ERROR_401},
    summary=UserConstants.MAKE_ADMIN,
)
async def update_me_admin_updater(
    session: SessionDep, user: CurrentUser
) -> User:
    """Для тестирования API.

    Только авторизированные.
    """
    return await user_service.make_me_admin(session, user=user)


@router.patch(
    '/{user_id}',
    response_model=UserRead,
    responses={
        **ResponsesSettings.ERROR_401,
        **ResponsesSettings.ERROR_422,
        **ResponsesSettings.ERROR_403,
        **ResponsesSettings.ERROR_404,
    },
    summary=UserConstants.PATCH_USER,
)
async def update_admin(
    user_id: int,
    obj_in: UserUpdateAdmin,
    session: SessionDep,
    current_admin: AdminUser,
) -> User:
    """Обновление пользователя по id.

    Только для админов.
    """
    user_to_update = await user_service.get_by_id(session, user_id)
    return await user_service.update_profile(session, user_to_update, obj_in)


@router.get(
    '',
    response_model=list[UserRead],
    responses={**ResponsesSettings.ERROR_401, **ResponsesSettings.ERROR_403},
    summary=UserConstants.GET_ALL,
)
async def get_multy(
    session: SessionDep,
    current_admin: AdminUser,
    is_active: bool | None = Query(None, description='Фильтр активности'),
) -> Sequence[User]:
    """Возвращает всех пользователей, доступн фильтр is_active.

    Только для админов.
    """
    return await user_service.get_multy(session, is_active=is_active)


@router.delete(
    '/me',
    status_code=status.HTTP_204_NO_CONTENT,
    summary=UserConstants.DEL_ME_SUM,
)
async def delete_me(session: SessionDep, user: CurrentUser) -> None:
    """Деактивирует аккаунт текущего пользователя.

    Только авторизированные.
    """
    await user_service.delete_my_account(session, user)
    return
