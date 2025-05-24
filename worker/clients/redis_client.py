import redis

from config import settings


redis = redis.asyncio.Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    decode_responses=True
)
