from datetime import date

from sqlalchemy import (
    CheckConstraint,
    Date,
    Enum,
    SmallInteger,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import IceBoxSlotConstants
from app.core.db import Base, Mixin
from app.core.enums import TimeSlot


class IceBoxSlot(Base, Mixin):
    """Создание слотов на ледовом катке."""

    week_day: Mapped[date] = mapped_column(Date, nullable=False)
    time_slot: Mapped[TimeSlot] = mapped_column(Enum(TimeSlot), nullable=False)
    capacity: Mapped[int] = mapped_column(
        SmallInteger, default=IceBoxSlotConstants.DEFAULT_CAPACITY
    )

    __table_args__ = (
        # В один день не может быть двух одинаковых временных слотов.
        UniqueConstraint('week_day', 'time_slot', name='unique_idx_day_time'),
        # Вместимость должна быть больше либо равна 0.
        CheckConstraint('capacity >=0', name='check_capacity_posotive'),
    )
