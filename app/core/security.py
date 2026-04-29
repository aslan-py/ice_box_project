from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings
from app.core.constants import LoguruSettings
from app.core.loguru_config import logger

ALGORITHM = 'HS256'


def create_access_token(user_id: int) -> str:
    """Создает JWT токен, упаковывая в него ID пользователя."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {'sub': str(user_id), 'exp': expire, 'type': 'access'}
    logger.debug(LoguruSettings.AUTH_TOKEN_CREATED.format(user_id))

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> int | None:
    """Декодирует токен и возвращает user_id, если токен валиден."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        user_id = payload.get('sub')
        if user_id is None:
            logger.warning(LoguruSettings.AUTH_TOKEN_INVALID_PAYLOAD)
            return None
        return int(user_id)
    except (jwt.PyJWTError, ValueError, TypeError) as e:
        logger.error(LoguruSettings.AUTH_TOKEN_ERROR.format(str(e)))
        return None
