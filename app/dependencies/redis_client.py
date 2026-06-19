from collections.abc import AsyncGenerator, Callable

from core.config import settings
from core.redis.client import RedisClient


def redis_client_factory(
    host: str = settings.redis.connection.host,
    port: int = settings.redis.connection.port,
    db: int = settings.redis.db.rate_limiter,
    decode_responses: bool = True,
) -> Callable[[], AsyncGenerator[RedisClient]]:
    async def get_redis_client() -> AsyncGenerator[RedisClient]:
        async with RedisClient(
            host=host,
            port=port,
            db=db,
            decode_responses=decode_responses,
        ) as redis_client:
            yield redis_client

    return get_redis_client


get_rate_limiter_redis_client = redis_client_factory(
    db=settings.redis.db.rate_limiter,
)

get_genre_redis_client = redis_client_factory(
    db=settings.redis.db.genres,
)

get_movie_redis_client = redis_client_factory(
    db=settings.redis.db.movies,
)

get_user_redis_client = redis_client_factory(
    db=settings.redis.db.users,
)

get_review_redis_client = redis_client_factory(
    db=settings.redis.db.reviews,
)

get_favorite_movie_redis_client = redis_client_factory(
    db=settings.redis.db.favorite_movies,
)

get_watch_history_redis_client = redis_client_factory(
    db=settings.redis.db.watch_history,
)

get_confirmation_code_redis_client = redis_client_factory(
    db=settings.redis.db.confirmation_codes,
)
