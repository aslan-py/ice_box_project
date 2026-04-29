from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import LoguruSettings, ResponseMessage
from app.core.loguru_config import logger
from app.crud.user import user_crud
from app.models.user import User
from app.schemas.user import UserUpdate, UserUpdateAdmin


class UserService:
    """Логика работы с User."""

    async def get_my_profile(self, user: User) -> User:
        """Возвращает текущего пользователя.

        Объект уже получен из зависимости CurrentUser.
        """
        return user

    async def get_by_id(self, session: AsyncSession, user_id: int) -> User:
        """Получает пользователя по ID или выбрасывает 404."""
        user = await user_crud.get(session, user_id)
        if not user:
            logger.warning(LoguruSettings.USER_NOT_FOUND.format(user_id))
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ResponseMessage.error_404,
            )
        return user

    async def update_profile(
        self,
        session: AsyncSession,
        user: User,
        obj_in: UserUpdate | UserUpdateAdmin,
    ) -> User:
        """Обновляет данные профиля пользователя.

        Methods:
        user_crud.check_user_exists — проверяет уникальность нового номера
            телефона или электронной почты в базе данных.
        user_crud.update — сохраняет обновленные данные пользователя
            в базу данных.

        """
        check_phone = (
            obj_in.phone
            if (obj_in.phone is not None and obj_in.phone != user.phone)
            else None
        )
        check_email = (
            obj_in.email
            if (obj_in.email is not None and obj_in.email != user.email)
            else None
        )

        if check_phone or check_email:
            conflict_user = await user_crud.check_user_exists(
                session, phone=check_phone, email=check_email
            )
            if conflict_user:
                logger.error(LoguruSettings.UPDATE_CONFLICT.format(user.id))
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ResponseMessage.error_user_400,
                )
        logger.info(LoguruSettings.UPDATE_SUCCESS.format(user.id))
        return await user_crud.update(
            session=session, schemas_in=obj_in, db_obj=user
        )

    async def delete_my_account(
        self, session: AsyncSession, user: User
    ) -> None:
        """Мягкое удаление пользователя.

        Меняет статус is_active на False через метод update.
        """
        logger.info(LoguruSettings.USER_DEACTIVATED.format(user.id))
        await user_crud.update(
            session=session, schemas_in={'is_active': False}, db_obj=user
        )

    async def get_multy(
        self, session: AsyncSession, is_active: bool | None = None
    ) -> Sequence[User]:
        """Получаем всех пользователей."""
        return await user_crud.get_multi(session=session, is_active=is_active)

    async def make_me_admin(
        self,
        session: AsyncSession,
        user: User,
    ) -> User:
        """Превращает пользователя в админа."""
        logger.warning(LoguruSettings.ADMIN_PROMOTED.format(user.name))
        return await user_crud.admin_maker(session, db_obj=user)


user_service = UserService()
