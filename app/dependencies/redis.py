from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from core.config import settings
from rate_limiter import RateLimiter
from redis_client import RedisClient


class RedisConnectionFactory:
    def __init__(
        self,
        host: str = settings.redis.connection.host,
        port: int = settings.redis.connection.port,
        decode_responses: bool = True,
        db: int = settings.redis.db.default,
    ):
        self.host = host
        self.port = port
        self.db = db
        self.decode_responses = decode_responses

    async def __aenter__(
        self,
        host: str = settings.redis.connection.host,
        port: int = settings.redis.connection.port,
        db: int = settings.redis.db.default,
        decode_responses: bool = True,
    ):
        async with RedisClient(
            host=self.host,
            port=self.port,
            db=db,
            decode_responses=self.decode_responses,
        ) as redis_client:
            yield redis_client

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Действия после выхода из асинхронного контекстного менеджера.
        """


async def get_redis_client(
    host: str = settings.redis.connection.host,
    port: int = settings.redis.connection.port,
    db: int = settings.redis.db.default,
    decode_responses: bool = True,
):
    async with RedisClient(
        host=host,
        port=port,
        db=db,
        decode_responses=decode_responses,
    ) as redis_client:
        yield redis_client


async def get_rate_limiter(
    redis_client: Annotated[
        RedisClient,
        Depends(get_redis_client),
    ],
):
    try:
        rate_limiter = RateLimiter(redis_client)
        yield rate_limiter
    finally:
        """
        Действия после возврата из yield.
        """


def rate_limit_dependencies_fabric(max_requests: int, time_period: int):
    async def dependency(
        request: Request,
        rate_limiter: Annotated[
            RateLimiter,
            Depends(get_rate_limiter),
        ],
    ):
        ip_address: str = request.client.host
        if await rate_limiter.is_limited(
            ip_address,
            request.url.path,
            max_requests,
            time_period,
        ):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too Many Requests",
            )

    return dependency


rate_limit_movie = rate_limit_dependencies_fabric(
    max_requests=5,
    time_period=3,
)
