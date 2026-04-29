import redis.asyncio as redis
from redis.asyncio import Redis

from app.core.config import settings

redis_client = redis.from_url(
    settings.REDIS_URL, encoding='utf-8', decode_responses=True
)


async def get_redis() -> Redis:
    """Возвращает клиент Redis для использования в сервисах."""
    return redis_client
