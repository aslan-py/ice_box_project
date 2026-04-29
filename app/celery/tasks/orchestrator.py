from app.celery.main import celery_app
from app.celery.tasks.email import send_email_task
from app.celery.tasks.sms import send_sms_task
from app.core.constants import AuthConstants, LoguruSettings
from app.core.loguru_config import logger


@celery_app.task(name='send_verification_flow')
def send_verification_flow(phone: str, email: str, code: str) -> str:
    """Управляет фоновой отправкой: СМС и Email.

    Methods:
    send_sms_task — отправляет код подтверждения через СМС-шлюз.
    send_email_task — отправляет сформированное сообщение с кодом
        на электронную почту.

    """
    # Готовим сообщение для почты
    email_msg = AuthConstants.code_msg.format(code)
    logger.info(LoguruSettings.FLOW_VERIFY_START.format(phone, email))
    try:
        # Для СМС обычно шлем чистый код или свое сообщение
        send_sms_task(int(phone), code)
    except Exception as e:
        logger.error(LoguruSettings.FLOW_SMS_ERROR.format(phone, str(e)))

    email_result = send_email_task(email, email_msg)
    if not email_result:
        logger.error(LoguruSettings.FLOW_EMAIL_ERROR.format(email))

    return AuthConstants.all_chanel_sent


@celery_app.task(name='send_cancellation_flow')
def send_cancellation_flow(
    users_data: list[dict], date_str: str, time_str: str
) -> str:
    """Диспетчер массовой рассылки об отмене.

    Methods:
    send_sms_task.delay — ставит в очередь задачу на отправку СМС
        об отмене сеанса.
    send_email_task.delay — ставит в очередь задачу на отправку Email
        с уведомлением и кастомным заголовком.

    """
    msg = AuthConstants.canseled_lot_msg.format(date_str, time_str)
    # Можно добавить отдельную константу для темы

    logger.info(LoguruSettings.FLOW_CANCEL_START.format(len(users_data)))

    for user in users_data:
        phone = user.get('phone')
        if phone:
            try:
                send_sms_task.delay(phone=int(phone), message=msg)
            except (ValueError, TypeError):
                logger.warning(LoguruSettings.FLOW_INVALID_PHONE.format(phone))

        email = user.get('email')
        if email:
            # Передаем текст и новую тему письма
            send_email_task.delay(email, msg, subject=AuthConstants.subject)

    return AuthConstants.sucess_notify.format(len(users_data))
