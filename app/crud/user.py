from typing import Sequence

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import Role
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """Управление пользователями: создание и мягкое удаление."""

    async def get_by_phone(
        self, session: AsyncSession, *, phone: str
    ) -> User | None:
        """Поиск пользователя по номеру телефона (индексированное поле)."""
        result = await session.execute(select(User).where(User.phone == phone))
        return result.scalar_one_or_none()

    async def check_user_exists(
        self,
        session: AsyncSession,
        *,
        phone: str | None = None,
        email: str | None = None,
    ) -> Sequence[User]:
        """Проверяет существование пользователя по телефону или почте."""
        if not phone and not email:
            return []

        filters = []
        if phone:
            filters.append(User.phone == phone)
        if email:
            filters.append(User.email == email)
        query = select(User).where(or_(*filters))
        result = await session.execute(query)
        return result.scalars().all()

    async def create_user(
        self, session: AsyncSession, phone: str, email: str, name: str
    ) -> User:
        """Создает пользователя только по телефону и имени."""
        db_obj = User(phone=phone, email=email, name=name)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def deactivate(self, session: AsyncSession, db_obj: User) -> User:
        """Мягкое удаление (деактивация) пользователя."""
        db_obj.is_active = False

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    async def admin_maker(
        self, session: AsyncSession, *, db_obj: User
    ) -> User:
        """Создает пользователя только по телефону и имени."""
        if db_obj.role == Role.USER:
            db_obj.role = Role.ADMIN

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


user_crud = CRUDUser(User)
