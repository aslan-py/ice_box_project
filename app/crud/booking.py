from typing import Any, Sequence

from sqlalchemy import Row, RowMapping, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.booking import Booking
from app.models.ice_box_slot import IceBoxSlot
from app.models.user import User
from app.schemas.booking import CreateBooking


class CRUDBooking(CRUDBase[Booking, CreateBooking, Any]):
    """Управление бронированиями через прямые SQL-связи (JOIN)."""

    async def create_with_slot_update(
        self, session: AsyncSession, *, slot: IceBoxSlot, user_id: int
    ) -> Booking:
        """Создает бронь и уменьшает вместимость слота в одной транзакции."""
        db_obj = Booking(slot_id=slot.id, user_id=user_id)
        slot.capacity -= 1

        session.add(db_obj)
        session.add(slot)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_user_bookings(
        self, session: AsyncSession, *, user_id: int
    ) -> Sequence[RowMapping]:
        """Получает список броней пользователя с данными слотов через JOIN."""
        query = (
            select(
                Booking.id,
                Booking.slot_id,
                Booking.user_id,
                IceBoxSlot.is_active,  # Явно берем статус из БРОНИ
                IceBoxSlot.week_day,
                IceBoxSlot.time_slot,
            )
            .join(IceBoxSlot, Booking.slot_id == IceBoxSlot.id)
            .where(Booking.user_id == user_id)
            .order_by(IceBoxSlot.week_day.desc())  # Свежие брони сверху
        )
        result = await session.execute(query)
        return result.mappings().all()

    async def get_by_user_and_slot(
        self, session: AsyncSession, *, user_id: int, slot_id: int
    ) -> Booking | None:
        """Проверяет наличие брони пользователя на конкретный слот."""
        result = await session.execute(
            select(self.model).where(
                self.model.user_id == user_id, self.model.slot_id == slot_id
            )
        )
        return result.scalar_one_or_none()

    async def get_notifiable_clients(
        self, session: AsyncSession, slot_id: int
    ) -> list[Row]:
        """Возвращает список номеров телефонов и email всех клиентов.

        С активной бронью на слот.
        """
        query = (
            select(User.phone, User.email)
            .join(Booking, User.id == Booking.user_id)
            .where(Booking.slot_id == slot_id)
            .where(Booking.is_active.is_(True))
        )
        result = await session.execute(query)
        return list(result.all())

    async def get_all_bookings_with_users(
        self, session: AsyncSession
    ) -> Sequence[RowMapping]:
        """Получает абсолютно все бронирования."""
        query = (
            select(
                IceBoxSlot.id.label('slot_id'),
                IceBoxSlot.week_day,
                IceBoxSlot.time_slot,
                IceBoxSlot.is_active,
                IceBoxSlot.capacity,
                Booking.id.label('booking_id'),
                Booking.user_id,
                User.name,
                User.phone,
            )
            .join(Booking, IceBoxSlot.id == Booking.slot_id)
            .join(User, Booking.user_id == User.id)
            .order_by(IceBoxSlot.week_day, IceBoxSlot.time_slot)
        )
        result = await session.execute(query)
        return result.mappings().all()


booking_crud = CRUDBooking(Booking)
