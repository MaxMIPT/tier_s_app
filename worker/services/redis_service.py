import json
import redis.asyncio as redis
from typing import Optional

from config import settings

async def publish_message(channel: str, message: str) -> None:
    async with redis.Redis(host=settings.redis.host, port=settings.redis.port) as r:
        await r.publish(channel, message)

async def publish(file_id: str, message: str):
    await redis.publish(channel=file_id, message=message)