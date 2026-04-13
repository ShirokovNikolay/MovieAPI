from typing import Annotated

from fastapi import Depends, Request

from core.config import settings
from core.exceptions.base import TooManyRequestsError
from rate_limiter import RateLimiter
from redis_client import RedisClient


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


def rate_limit_dependency_factory(max_requests: int, time_period: int):
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
            raise TooManyRequestsError(
                "Too many requests to this source. Wait a little while.",
            )

    return dependency


check_rate_limit_auth = rate_limit_dependency_factory(
    max_requests=15,
    time_period=5,
)

check_rate_limit_not_auth = rate_limit_dependency_factory(
    max_requests=6,
    time_period=5,
)
