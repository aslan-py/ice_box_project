from celery import Celery

from app.core.config import settings

celery_app = Celery(
    'ice_skating_tasks',
    broker=settings.celery_broker_url,
    backend='rpc://',
    include=[
        'app.celery.tasks.sms',
        'app.celery.tasks.email',
        'app.celery.tasks.orchestrator',
    ],
)

# Настраиваем очереди и автопоиск тасок
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
)
