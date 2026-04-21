from fastapi import APIRouter, Depends, status

from dependencies.annotations.cache_services import ReviewCacheServiceDep
from dependencies.annotations.validators import PaginationPageDep, PaginationSizeDep
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
    review_cache_service: ReviewCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
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
    review_cache_service: ReviewCacheServiceDep,
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
    review_cache_service: ReviewCacheServiceDep,
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
    review_cache_service: ReviewCacheServiceDep,
) -> ReviewResponseList:
    return await review_cache_service.get_top_oldest_movie_reviews(movie_id, limit)
