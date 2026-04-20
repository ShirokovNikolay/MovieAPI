from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from cache_services import ReviewCacheService
from dependencies.cache_services import get_review_cache_service
from dependencies.rate_limiter import check_rate_limit_not_auth
from schemas.review import ReviewResponseList

router = APIRouter(
    prefix="/{movie_id}",
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)


@router.get(
    "/",
    response_model=ReviewResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_movie_reviews(
    movie_id: int,
    review_cache_service: Annotated[
        ReviewCacheService,
        Depends(get_review_cache_service),
    ],
    size: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
) -> ReviewResponseList:
    return await review_cache_service.get_movie_reviews(movie_id, size, page)


@router.get(
    "/top-rated/{limit}",
    response_model=ReviewResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_top_rating_movie_reviews(
    movie_id: int,
    limit: int,
    review_cache_service: Annotated[
        ReviewCacheService,
        Depends(get_review_cache_service),
    ],
) -> ReviewResponseList:
    return await review_cache_service.get_top_rating_movie_reviews(movie_id, limit)


@router.get(
    "/top-newest/{limit}",
    response_model=ReviewResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_top_newest_movie_reviews(
    movie_id: int,
    limit: int,
    review_cache_service: Annotated[
        ReviewCacheService,
        Depends(get_review_cache_service),
    ],
) -> ReviewResponseList:
    return await review_cache_service.get_top_newest_movie_reviews(movie_id, limit)


@router.get(
    "/top-oldest/{limit}",
    response_model=ReviewResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_top_oldest_movie_reviews(
    movie_id: int,
    limit: int,
    review_cache_service: Annotated[
        ReviewCacheService,
        Depends(get_review_cache_service),
    ],
) -> ReviewResponseList:
    return await review_cache_service.get_top_oldest_movie_reviews(movie_id, limit)
