from pydantic import BaseModel, EmailStr, Field

from app.core.constants import AuthConstants, UserConstants
from app.schemas.types import PhoneFormat


class AuthRequestCode(BaseModel):
    """Схема для первого шага: запрос СМС по номеру телефона или почте."""

    phone: PhoneFormat = Field(..., description=UserConstants.DESCR_PHONE)
    email: EmailStr


class AuthVerifyCode(BaseModel):
    """Схема для второго шага: проверка кода и получение токена."""

    phone: PhoneFormat = Field(..., description=UserConstants.DESCR_PHONE)
    code: str = Field(
        ..., min_length=4, max_length=4, description='Код из СМС (4 цифры)'
    )


class AuthResponse(BaseModel):
    """Схема успешного ответа на запрос кода."""

    status: str = Field(..., examples=[AuthConstants.sms_status_code])
    message: str = Field(..., examples=[AuthConstants.sms_status_msg])


class Token(BaseModel):
    """Схема ответа с JWT токеном."""

    access_token: str
    token_type: str = 'Bearer'


class TokenData(BaseModel):
    """Данные, зашитые внутри токена (payload)."""

    user_id: int | None = None
