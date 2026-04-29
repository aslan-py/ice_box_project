from smsaero import SmsAero

from app.core.config import settings
from app.core.constants import LoguruSettings
from app.core.loguru_config import logger


def send_sms(phone: int, message: str) -> dict:
    """Функция отправки смс."""
    api = SmsAero(settings.smsaero_email, settings.smsaero_api_key)
    logger.info(LoguruSettings.SMS_ATTEMPT.format(phone))
    return api.send_sms(phone, message)
