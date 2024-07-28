import redis.asyncio as redis

from settings import settings

# Redis client instance
client = redis.Redis(host=settings.redis.host, port=settings.redis.port)
