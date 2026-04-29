from sqlalchemy import CheckConstraint, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, Mixin
from app.core.enums import Role


class User(Base, Mixin):
    """Модель пользователя."""

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    role: Mapped[Role] = mapped_column(
        Enum(Role), default=Role.USER, server_default=Role.USER.value
    )

    __table_args__ = (
        CheckConstraint('LENGTH(name) >= 3', name='check_name_len'),
    )
