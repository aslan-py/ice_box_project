import json
import random

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.celery.tasks.orchestrator import send_verification_flow
from app.core.constants import AuthConstants, LoguruSettings
from app.core.loguru_config import logger
from app.core.redis_config import redis_client
from app.core.security import create_access_token
from app.crud.user import user_crud
from app.schemas.auth import AuthVerifyCode, Token


class AuthService:
    """Логика вторизации."""

    OTP_EXPIRY = AuthConstants.OTP_EXPIRY  # Код живет 5 минут (300 секунд)

    async def request_sms_code(
        self, session: AsyncSession, phone: str, email: str
    ) -> dict:
        """Генерирует одноразовый код для регистрации или входа.

        Methods:
        user_crud.check_user_exists — проверяет наличие пользователей с данным
            номером телефона или почтой для обеспечения безопасности.
        redis_client.set — сохраняет сгенерированный код и email в кеш с
            заданным временем жизни (TTL).
        send_verification_flow.delay — инициирует фоновую задачу по отправке
            кода через доступные каналы связи (SMS, Email).

        """
        users = await user_crud.check_user_exists(
            session, phone=phone, email=email
        )

        if len(users) > 1:
            logger.error(
                LoguruSettings.AUTH_SECURITY_WARN.format(phone, email)
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AuthConstants.security_error,
            )
        if len(users) == 1:
            user = users[0]
            if user.phone != phone or user.email != email:
                logger.warning(LoguruSettings.AUTH_ALREADY_USED.format(phone))
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=AuthConstants.already_used,
                )
            target_phone, target_email = user.phone, user.email
        else:
            target_phone, target_email = phone, email

        code = str(random.randint(1000, 9999))
        otp_data = {'code': code, 'email': target_email}

        await redis_client.set(
            name=f'otp:{target_phone}',
            value=json.dumps(otp_data),
            ex=self.OTP_EXPIRY,
        )
        # print('---------------', code)
        logger.info(LoguruSettings.AUTH_CODE_SENT.format(target_phone))
        send_verification_flow.delay(int(target_phone), target_email, code)

        return AuthConstants.sms_status

    async def verify_code_and_login(
        self,
        session: AsyncSession,
        auth_data: AuthVerifyCode,
        name_if_new: str = AuthConstants.NEW_DEFAULT_NAME,
    ) -> Token:
        """Проверяет код из Redis и выдает JWT.

        Methods:
        redis_client.get — извлекает временные данные (код и email) по номеру
            телефона из кеша.
        user_crud.get_by_phone — выполняет поиск пользователя в базе данных
            для аутентификации.
        user_crud.create_user — регистрирует нового пользователя, если он не
            был найден в системе.
        redis_client.delete — удаляет использованный код из кеша для
            предотвращения повторной авторизации.
        create_access_token — формирует подписанный JWT для доступа к API.

        """
        phone = auth_data.phone
        code = auth_data.code

        # 1. Достаем код из Redis
        raw_data = await redis_client.get(f'otp:{phone}')

        if not raw_data:
            logger.warning(LoguruSettings.AUTH_OTP_EXPIRED.format(phone))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AuthConstants.error_auth_400,
            )

        otp_cache = json.loads(raw_data)
        saved_code = otp_cache.get('code')
        saved_email = otp_cache.get('email')

        if saved_code != code:
            logger.warning(LoguruSettings.AUTH_INVALID_CODE.format(phone))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AuthConstants.error_auth_400_wrong,
            )

        # 2. Работа с пользователем
        user = await user_crud.get_by_phone(session, phone=phone)
        if not user:
            user = await user_crud.create_user(
                session, phone=phone, email=saved_email, name=name_if_new
            )
            logger.info(LoguruSettings.AUTH_USER_CREATED.format(phone))

        # 3. Успех — удаляем код, чтобы нельзя было использовать дважды
        await redis_client.delete(f'otp:{phone}')

        # 4. Генерируем токен
        access_token = create_access_token(user_id=user.id)

        logger.info(LoguruSettings.AUTH_SUCCESS.format(phone))
        return Token(access_token=access_token)


auth_service = AuthService()
