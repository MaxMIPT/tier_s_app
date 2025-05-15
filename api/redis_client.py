import redis

from config import settings


redis = redis.asyncio.Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    decode_responses=True
)


async def subscribe(file_id: str):
    pubsub = redis.pubsub()
    await pubsub.subscribe(file_id)
    async for message in pubsub.listen():
        if message['type'] == 'message':
            yield message['data']
