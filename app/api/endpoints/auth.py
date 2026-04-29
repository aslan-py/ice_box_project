from fastapi import APIRouter

from app.api.deps import SessionDep
from app.api.responses import ResponsesSettings
from app.core.constants import AuthConstants
from app.schemas.auth import (
    AuthRequestCode,
    AuthResponse,
    AuthVerifyCode,
    Token,
)
from app.services.auth import auth_service

router = APIRouter()


@router.post(
    '/request-code',
    summary=AuthConstants.request_summary,
    responses=ResponsesSettings.ERROR_422,
    response_model=AuthResponse,
)
async def request_code(data: AuthRequestCode, session: SessionDep) -> dict:
    """Шаг 1: Пользователь вводит телефон и email - получает проверочный код.

    Доступно всем.
    """
    return await auth_service.request_sms_code(session, data.phone, data.email)


@router.post(
    '/verify',
    response_model=Token,
    summary=AuthConstants.verify_summary,
    responses=ResponsesSettings.ERROR_422,
)
async def verify_code(data: AuthVerifyCode, session: SessionDep) -> Token:
    """Шаг 2: Пользователь вводит телефон и код из СМС или почты.

    Если код верный — возвращаем JWT токен.
    """
    return await auth_service.verify_code_and_login(session, data)
