from fastapi import APIRouter, status

from app.api.deps import AdminUser, CurrentUser, SessionDep
from app.api.responses import ResponsesSettings
from app.core.constants import BookingConstants
from app.models.booking import Booking
from app.schemas.booking import (
    AdminSlotReport,
    BookingResponse,
    CreateBooking,
    MyBooking,
)
from app.services.booking import booking_service

router = APIRouter()


@router.post(
    '/',
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
    summary=BookingConstants.SUM_POST_BOOK,
    responses={
        **ResponsesSettings.ERROR_401,
        **ResponsesSettings.ERROR_422,
        **ResponsesSettings.ERROR_404,
    },
)
async def create_booking(
    obj_in: CreateBooking, session: SessionDep, user: CurrentUser
) -> Booking:
    """Бронирование сеанса на катке.

    Только авторизированные.
    """
    return await booking_service.create_booking(session, user, obj_in)


@router.get(
    '/me',
    response_model=list[MyBooking],
    summary=BookingConstants.SUM_GET_MУ,
    responses={
        **ResponsesSettings.ERROR_401,
    },
)
async def get_my_bookings(
    session: SessionDep, user: CurrentUser
) -> list[MyBooking]:
    """Просмотр своих бронирований.

    Только авторизированные.
    """
    return await booking_service.get_my_bookings(session, user)


@router.get(
    '/all',
    response_model=list[AdminSlotReport],
    summary=BookingConstants.SUM_GET_ALL_BOOK,
    responses={
        **ResponsesSettings.ERROR_401,
        **ResponsesSettings.ERROR_403,
    },
)
async def get_all_bookings_admin(
    session: SessionDep, current_admin: AdminUser
) -> list[AdminSlotReport]:
    """Показать  все слоты с группировкой.

    Только админы.
    """
    return await booking_service.get_admin_booking_report(session)


@router.delete(
    '/{booking_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary=BookingConstants.SUM_DEL_BOOK,
    responses={
        **ResponsesSettings.ERROR_401,
        **ResponsesSettings.ERROR_422,
        **ResponsesSettings.ERROR_404,
    },
)
async def cancel_booking(
    booking_id: int, session: SessionDep, user: CurrentUser
) -> None:
    """Отмена бронирования.

    Только авторизированные.
    """
    await booking_service.cancel_booking(session, user, booking_id)
    return
