from core.config import settings
from redis_client import RedisClient


def redis_client_factory(
    host: str = settings.redis.connection.host,
    port: int = settings.redis.connection.port,
    db: int = settings.redis.db.rate_limiter,
    decode_responses: bool = True,
):
    async def get_redis():
        async with RedisClient(
            host=host,
            port=port,
            db=db,
            decode_responses=decode_responses,
        ) as redis_client:
            yield redis_client

    return get_redis


get_redis_client_for_rate_limiter = redis_client_factory(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.rate_limiter,
    decode_responses=True,
)
