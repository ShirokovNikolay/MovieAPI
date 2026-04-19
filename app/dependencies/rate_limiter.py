from typing import Annotated, cast

from fastapi import Depends
from starlette.requests import Request

from core.exceptions.base import TooManyRequestsError
from dependencies.redis_client import get_redis_client_for_rate_limiter
from core.redis.rate_limiter import RateLimiter
from core.redis.client import RedisClient


def rate_limit_dependency_factory(max_requests: int, time_period: int):
    async def dependency(
        request: Request,
        rate_limiter: Annotated[
            RateLimiter,
            Depends(get_rate_limiter),
        ],
    ):
        assert request.client is not None
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


async def get_rate_limiter(
    redis_client: Annotated[
        RedisClient,
        Depends(get_redis_client_for_rate_limiter),
    ],
):
    try:
        rate_limiter = RateLimiter(redis_client)
        yield rate_limiter
    finally:
        """
        Действия после возврата из yield.
        """


check_rate_limit_auth = rate_limit_dependency_factory(
    max_requests=15,
    time_period=5,
)
check_rate_limit_not_auth = rate_limit_dependency_factory(
    max_requests=6,
    time_period=5,
)
