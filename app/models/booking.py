from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, Mixin


class Booking(Base, Mixin):
    """Таблица для записи конкретных пользователей в слоты."""

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE', name='fk_booking_user_id'),
        nullable=False,
    )
    slot_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            'iceboxslot.id', ondelete='CASCADE', name='fk_booking_ice_box_slot'
        ),
        nullable=False,
    )

    __table_args__ = (
        # один юзер — один слот.
        UniqueConstraint('user_id', 'slot_id', name='unique_user_booking'),
    )
