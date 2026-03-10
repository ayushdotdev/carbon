import redis.asyncio as redis

from app.config import settings

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    username="carbon",
    password=settings.redis_pass,
    decode_responses=True,
)
