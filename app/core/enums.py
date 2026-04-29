from enum import StrEnum


class TimeSlot(StrEnum):
    """Временные слоты для бронирования сеанса ледового катка."""

    eleven = '11:00'
    twelve = '12:00'
    thirteen = '13:00'


class Role(StrEnum):
    """Варианты ролей."""

    ADMIN = 'ADMIN'
    USER = 'USER'
