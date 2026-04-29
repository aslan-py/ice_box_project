import asyncio

from fastapi_mail import FastMail, MessageSchema, MessageType

from app.celery.main import celery_app
from app.core.config import settings
from app.core.constants import AuthConstants, LoguruSettings
from app.core.loguru_config import logger


@celery_app.task(name='send_email_task')
def send_email_task(
    email: str, message_text: str, subject: str = AuthConstants.subject_msg
) -> bool:
    """Чистый отправитель Email.

    Methods:
    FastMail.send_message — формирует и отправляет письмо через SMTP
        сервер, используя предоставленный конфиг.

    """
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=message_text,
        subtype=MessageType.plain,
    )
    fm = FastMail(settings.mail_config)
    logger.info(LoguruSettings.EMAIL_ATTEMPT.format(email))
    try:
        asyncio.run(fm.send_message(message))
        logger.info(LoguruSettings.EMAIL_SENT_SUCCESS.format(email))
        return True
    except Exception as e:
        logger.error(LoguruSettings.EMAIL_ERROR.format(email, str(e)))
        return False
