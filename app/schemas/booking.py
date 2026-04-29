from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import BookingConstants
from app.core.enums import TimeSlot


class BookingBase(BaseModel):
    """Базовая схема бронирования."""

    slot_id: int = Field(..., gt=0, description=BookingConstants.DESCR_SLOT_ID)


class CreateBooking(BookingBase):
    """Схема для создания новой брони.

    Используется в POST-запросах. user_id не передается пользователем,
    а извлекается из системы аутентификации на сервере.
    """

    pass


class BookingResponse(BookingBase):
    """Схема для базового ответа сервера после создания брони.

    Содержит системные поля, такие как ID записи и статус активности.
    """

    id: int = Field(..., description=BookingConstants.DESCR_BOOKING_ID)
    user_id: int = Field(..., description=BookingConstants.DESCR_USER_ID)
    is_active: bool = Field(..., description=BookingConstants.DESCR_IS_ACTIVE)

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class MyBooking(BookingResponse):
    """Схема для отображения бронирований в личном кабинете пользователя.

    Включает дополнительные данные о времени и дате сеанса,
    чтобы пользователю не нужно было знать ID слота.
    """

    week_day: date = Field(..., description=BookingConstants.DESCR_WEEK_DAY)
    time_slot: TimeSlot = Field(
        ..., description=BookingConstants.DESCR_TIME_SLOT
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra=BookingConstants.BOOKING_EXAMPLE,  # type: ignore
    )


class UserBookingInfo(BaseModel):
    """Информация о пользователе внутри админского отчета."""

    booking_id: int
    user_id: int
    phone: str
    name: str


class AdminSlotReport(BaseModel):
    """Слот с вложенным списком забронировавших его людей."""

    slot_id: int
    week_day: date
    time_slot: TimeSlot
    is_active: bool
    capacity: int
    # Тот самый вложенный список
    bookings: list[UserBookingInfo]
