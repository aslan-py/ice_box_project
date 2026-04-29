from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import BookingConstants, LoguruSettings
from app.core.loguru_config import logger
from app.crud.booking import booking_crud
from app.crud.ice_box_slot import ice_box_slot_crud
from app.models.booking import Booking
from app.models.user import User
from app.schemas.booking import (
    AdminSlotReport,
    CreateBooking,
    MyBooking,
    UserBookingInfo,
)


class BookingService:
    """Логика бронирования слотов."""

    async def create_booking(
        self, session: AsyncSession, user: User, obj_in: CreateBooking
    ) -> Booking:
        """Создает бронирование и списывает место из слота.

        Methods:
        ice_box_slot_crud.get — проверяет существование целевого слота
            в базе данных.
        booking_crud.get_by_user_and_slot — проверяет наличие у пользователя
            повторного бронирования на то же время.
        booking_crud.create_with_slot_update — создает запись бронирования и
            уменьшает количество свободных мест в слоте.

        """
        # 1. Проверяем слот
        slot = await ice_box_slot_crud.get(session, obj_id=obj_in.slot_id)
        if not slot:
            logger.warning(
                LoguruSettings.BOOK_SLOT_NOT_FOUND.format(
                    obj_in.slot_id, user.id
                )
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=BookingConstants.ERR_BOOK_NOT_FOUND,
            )
        if not slot.is_active:
            logger.warning(
                LoguruSettings.BOOK_SLOT_INACTIVE.format(slot.id, user.id)
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=BookingConstants.ERR_BOOK_NOT_AVAILABLE,
            )
        # 2. Проверяем свободные места (capacity теперь это остаток мест)
        if slot.capacity <= 0:
            logger.warning(LoguruSettings.BOOK_NO_CAPACITY.format(slot.id))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=BookingConstants.ERR_BOOK_NOT_FREE,
            )
        # 3. Проверяем, не забронировал ли юзер этот слот ранее
        existing_booking = await booking_crud.get_by_user_and_slot(
            session, user_id=user.id, slot_id=slot.id
        )
        if existing_booking:
            logger.warning(
                LoguruSettings.BOOK_DUPLICATE.format(user.id, slot.id)
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=BookingConstants.ERR_BOOK_DOUBLE,
            )
        # 4. Создаем слот
        logger.info(LoguruSettings.BOOK_CREATED.format(user.id, slot.id))
        return await booking_crud.create_with_slot_update(
            session=session, slot=slot, user_id=user.id
        )

    async def get_my_bookings(
        self, session: AsyncSession, user: User
    ) -> Sequence[MyBooking]:
        """Возвращает список бронирований с данными слота."""
        return await booking_crud.get_user_bookings(session, user_id=user.id)

    async def cancel_booking(
        self, session: AsyncSession, user: User, booking_id: int
    ) -> None:
        """Отменяет бронирование и возвращает место в слот.

        Methods:
        booking_crud.get — получает объект бронирования из базы данных для
            проверки его существования.
        ice_box_slot_crud.get — находит соответствующий временной слот для
            корректировки количества свободных мест.
        booking_crud.remove — удаляет запись о бронировании из базы данных.

        """
        booking = await booking_crud.get(session, obj_id=booking_id)

        if not booking:
            logger.warning(LoguruSettings.CANCEL_NOT_FOUND.format(booking_id))
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=BookingConstants.ERR_404_BOOK,
            )

        if booking.user_id != user.id:
            logger.error(
                LoguruSettings.CANCEL_FORBIDDEN.format(user.id, booking_id)
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=BookingConstants.ERR_403_BOOK,
            )

        # Возвращаем место обратно в слот
        slot = await ice_box_slot_crud.get(session, obj_id=booking.slot_id)
        if slot:
            slot.capacity += 1
            session.add(slot)
        logger.info(LoguruSettings.CANCEL_SUCCESS.format(booking_id, user.id))
        await booking_crud.remove(session, obj_id=booking_id)

    async def get_admin_booking_report(
        self, session: AsyncSession
    ) -> list[AdminSlotReport]:
        """Формирует отчет: один слот - список пользователей."""
        rows = await booking_crud.get_all_bookings_with_users(session)

        # Используем словарь для группировки по slot_id
        grouped = {}

        for row in rows:
            s_id = row['slot_id']

            if s_id not in grouped:
                # Если слота еще нет в словаре, создаем "шапку"
                grouped[s_id] = AdminSlotReport(
                    slot_id=s_id,
                    week_day=row['week_day'],
                    time_slot=row['time_slot'],
                    is_active=row['is_active'],
                    capacity=row['capacity'],
                    bookings=[],
                )

            # Добавляем пользователя во вложенный список этого слота
            grouped[s_id].bookings.append(
                UserBookingInfo(
                    booking_id=row['booking_id'],
                    user_id=row['user_id'],
                    phone=row['phone'],
                    name=row['name'],
                )
            )

        # Возвращаем только значения словаря (список объектов AdminSlotReport)
        return list(grouped.values())


booking_service = BookingService()
