from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import IceBoxSlotConstants
from app.core.enums import TimeSlot
from app.schemas.types import FutureDate, SlotCapacity


class IceBoxSlotBase(BaseModel):
    """Базовая схема слота с общими полями."""

    week_day: date = Field(..., description=IceBoxSlotConstants.DESCR_WEEK_DAY)
    time_slot: TimeSlot = Field(
        ..., description=IceBoxSlotConstants.DESCR_TIME_SLOT
    )
    capacity: SlotCapacity = Field(
        IceBoxSlotConstants.DEFAULT_CAPACITY,
        ge=IceBoxSlotConstants.MIN_CAPACITY,
        description=IceBoxSlotConstants.DESCR_CAPACITY,
    )


class IceBoxSlotCreate(IceBoxSlotBase):
    """Схема для создания нового слота администратором.

    Включает все базовые поля. Вместимость по умолчанию — 20 человек.
    """

    week_day: FutureDate = Field(
        ..., description=IceBoxSlotConstants.DESCR_WEEK_DAY
    )


class IceBoxSlotUpdate(BaseModel):
    """Схема для частичного обновления данных слота.

    Все поля необязательны, что позволяет менять только нужные параметры,
    например, только вместимость или статус активности.
    """

    week_day: FutureDate | None = Field(
        None, description=IceBoxSlotConstants.DESCR_WEEK_DAY
    )
    time_slot: TimeSlot | None = Field(
        None, description=IceBoxSlotConstants.DESCR_TIME_SLOT
    )
    capacity: SlotCapacity | None = Field(
        None,
        ge=IceBoxSlotConstants.MIN_CAPACITY,
        description=IceBoxSlotConstants.DESCR_CAPACITY,
    )
    is_active: bool | None = Field(
        None, description=IceBoxSlotConstants.DESCR_IS_ACTIVE
    )


class IceBoxSlotResponse(IceBoxSlotBase):
    """Схема для ответа сервера с данными о слоте."""

    capacity: int = Field(..., description=IceBoxSlotConstants.DESCR_CAPACITY)
    id: int = Field(..., description=IceBoxSlotConstants.DESCR_ID)
    is_active: bool = Field(
        ..., description=IceBoxSlotConstants.DESCR_IS_ACTIVE
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra=IceBoxSlotConstants.ICE_EXAMPLE,  # type: ignore
    )
