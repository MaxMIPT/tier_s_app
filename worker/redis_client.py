import redis

from config import settings


redis = redis.asyncio.Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    decode_responses=True
)


async def publish(file_id: str, message: str):
    await redis.publish(channel=file_id, message=message)
