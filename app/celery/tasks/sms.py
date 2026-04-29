from app.celery.main import celery_app
from app.core.constants import AuthConstants, LoguruSettings
from app.core.loguru_config import logger
from app.core.sms_sender import send_sms


@celery_app.task(name='send_sms_task')
def send_sms_task(
    phone: int, code: str | None = None, message: str | None = None
) -> dict:
    """Универсальный исполнитель отправки СМС."""
    if code:
        msg = AuthConstants.code_msg.format(code)
    elif message:
        msg = message
    else:
        logger.error(LoguruSettings.SMS_TASK_PARAMS_ERROR.format(phone))
        raise ValueError(AuthConstants.sms_error_msg)
    logger.info(LoguruSettings.SMS_TASK_STARTED.format(phone))

    return send_sms(phone, msg)
