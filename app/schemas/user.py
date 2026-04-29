from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.constants import UserConstants
from app.core.enums import Role
from app.schemas.types import NameFormat, PhoneFormat


class UserBase(BaseModel):
    """Базовая схема пользователя с общими полями."""

    name: NameFormat = Field(
        ...,
        min_length=UserConstants.USERNAME_MIN_LENGTH,
        max_length=UserConstants.USERNAME_MAX_LENGTH,
        description=UserConstants.USERNAME,
    )
    phone: PhoneFormat = Field(..., description=UserConstants.DESCR_PHONE)
    email: EmailStr


class UserRead(UserBase):
    """Схема для возврата данных пользователя.

    Содержит системный ID, роль и статус активности.
    """

    id: int = Field(..., description=UserConstants.USER_ID)
    role: Role = Field(..., description=UserConstants.ROLE)
    is_active: bool = Field(..., description=UserConstants.IS_ACTIVE)

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra=UserConstants.USER_EXAMPLE,  # type: ignore
    )


class UserCreate(UserBase):
    """Схема для регистрации нового пользователя."""

    pass


class UserUpdate(BaseModel):
    """Схема для обычного пользователя."""

    name: NameFormat | None = Field(
        None,
        min_length=UserConstants.USERNAME_MIN_LENGTH,
        max_length=UserConstants.USERNAME_MAX_LENGTH,
    )
    phone: PhoneFormat | None = Field(
        None, description=UserConstants.DESCR_PHONE
    )
    email: EmailStr | None = None
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')


class UserUpdateAdmin(UserUpdate):
    """Схема для администратора.

    Наследует поля 'name' и 'phone', но добавляет возможность менять роль
    и статус активности пользователя.
    """

    role: Role | None = Field(None, description=UserConstants.ROLE_UPDATE)
    is_active: bool | None = Field(
        None, description=UserConstants.STATUS_UPDATE
    )
