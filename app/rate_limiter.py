import time
import random

from redis_client import RedisClient


class RateLimiter:
    def __init__(self, redis: RedisClient):
        self.redis_client = redis

    async def is_limited(
        self,
        ip_address: str,
        endpoint: str,
        max_requests: int = 3,
        time_period: int = 5,
    ) -> bool:
        key = f"rate_limiter:{endpoint}:{ip_address}"
        current_time = time.time()
        start_time = current_time - time_period
        member = f"{current_time}:{random.randint(1, 10 ** 6)}"
        await self.redis_client.zremrangebyscore(key, 0, start_time)
        await self.redis_client.zadd(key, {member: current_time})
        current_requests = await self.redis_client.zcard(key)
        await self.redis_client.expire(key, time_period)
        return max_requests < current_requests
