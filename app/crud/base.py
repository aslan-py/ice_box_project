from typing import Any, Sequence

from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base


class CRUDBase[
    ModelType: Base,
    CreateSchema: BaseModel,
    UpdateSchema: BaseModel,
]:
    """Базовый класс для реализации стандартных операций CRUD."""

    def __init__(self, model: type[ModelType]) -> None:
        """Инициализирует объект CRUD."""
        self.model = model

    async def get(
        self, session: AsyncSession, obj_id: int
    ) -> ModelType | None:
        """Получает одну запись из базы данных по её ID.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            obj_id (int): Идентификатор искомой записи.

        Returns:
            ModelType | None: Объект модели, если найден, иначе None.

        """
        return await session.get(self.model, obj_id)

    async def get_multi(
        self, session: AsyncSession, is_active: bool | None = None
    ) -> Sequence[ModelType]:
        """Получает список записей.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            is_active(bool): Статус активности.

        Returns:
            Sequence[ModelType]: Список найденных объектов.

        """
        query = select(self.model)

        if is_active is not None:
            query = query.where(self.model.is_active == is_active)

        result = await session.execute(query)
        return result.scalars().all()

    async def create(
        self, session: AsyncSession, schemas_in: CreateSchema
    ) -> ModelType:
        """Создает новую запись в базе данных.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            schemas_in (CreateSchemaType): Pydantic-схема
                с данными для создания.

        Returns:
            ModelType: Созданный объект модели.

        """
        obj_in_data = schemas_in.model_dump()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        session: AsyncSession,
        schemas_in: UpdateSchema | dict[str, Any],
        db_obj: ModelType,
    ) -> ModelType:
        """Обновляет существующую запись в базе данных.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            schemas_in (UpdateSchemaType | dict):
                Новые данные (схема или словарь).
            db_obj (ModelType): Текущий объект из базы данных.

        Returns:
            ModelType: Обновленный объект модели.

        """
        if isinstance(schemas_in, dict):
            update_data = schemas_in
        else:
            update_data = schemas_in.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if hasattr(db_obj, key):
                setattr(db_obj, key, value)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self, session: AsyncSession, obj_id: int
    ) -> ModelType | None:
        """Полностью удаляет запись из базы данных (Hard Delete).

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            obj_id (int): ID записи для удаления.

        Returns:
            ModelType | None: Удаленный объект или None, если не найден.

        """
        result = await session.execute(
            delete(self.model)
            .where(self.model.id == obj_id)  # type: ignore
            .returning(self.model)
        )
        await session.commit()
        return result.scalar_one_or_none()
