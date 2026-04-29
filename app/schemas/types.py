import re
from datetime import date
from typing import Annotated

from pydantic import AfterValidator, EmailStr

from app.core.constants import IceBoxSlotConstants, UserConstants


def validate_phone(phone: str) -> str:
    """Валидация телефона.

    - Всего 11 цифр без пробелов и черточек, слитно, начинаются с 7.
    """
    if not re.match(UserConstants.PHONE_PATTERN, phone):
        raise ValueError(UserConstants.PHONE_ERR)
    return phone


def validate_name(name: str) -> str:
    """Валидация имени.

    - Только буквы.
    - Автоматическое приведение к заглавной первой букве.
    """
    if not re.match(UserConstants.NAME_PATTERN, name):
        raise ValueError(UserConstants.NAME_ERR)
    return name.capitalize()


def validate_not_past_date(v: date) -> date:
    """Проверка, что дата не в прошлом."""
    if v < date.today():
        raise ValueError(IceBoxSlotConstants.ERR_PAST_DATE)
    return v


def validate_max_capacity(capacity: int) -> int:
    """Проверка максимальной вместимости."""
    if capacity > IceBoxSlotConstants.DEFAULT_CAPACITY:
        raise ValueError(IceBoxSlotConstants.ERR_MAX_CAPACITY)
    if capacity <= 0:
        raise ValueError(IceBoxSlotConstants.ERR_MIN_CAPACITY)
    return capacity


PhoneFormat = Annotated[str, AfterValidator(validate_phone)]
NameFormat = Annotated[str, AfterValidator(validate_name)]
FutureDate = Annotated[date, AfterValidator(validate_not_past_date)]
SlotCapacity = Annotated[int, AfterValidator(validate_max_capacity)]
EmailFormat = Annotated[EmailStr, AfterValidator(lambda v: v.lower())]
