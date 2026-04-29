from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

from app.core.config import settings


class Mixin:
    """Добавляет название таблиц, id - primary key и статус активности."""

    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)
    is_active: Mapped[bool] = mapped_column(default=True)


class Base(DeclarativeBase):
    """Базовый класс для моделей."""

    pass


engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный генератор сессий."""
    async with AsyncSessionLocal() as async_session:
        try:
            yield async_session
        except Exception:
            await async_session.rollback()
            raise
        finally:
            await async_session.close()


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
