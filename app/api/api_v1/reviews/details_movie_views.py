from fastapi import APIRouter, Depends, status

from dependencies.annotations.cache_services import ReviewCacheServiceDep
from dependencies.annotations.validators import PaginationPageDep, PaginationSizeDep
from dependencies.rate_limiter import check_rate_limit_not_auth
from schemas.review import ReviewWithUserResponseList

router = APIRouter(
    prefix="/{movie_id}",
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)


@router.get(
    "/",
    response_model=ReviewWithUserResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_movie_reviews(
    movie_id: int,
    review_cache_service: ReviewCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> ReviewWithUserResponseList:
    return await review_cache_service.get_movie_reviews(movie_id, size, page)


@router.get(
    "/low-rated",
    response_model=ReviewWithUserResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_low_rated_movie_reviews(
    movie_id: int,
    review_cache_service: ReviewCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> ReviewWithUserResponseList:
    return await review_cache_service.get_low_rated_movie_reviews(movie_id, size, page)


@router.get(
    "/top-rated",
    response_model=ReviewWithUserResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_top_rated_movie_reviews(
    movie_id: int,
    review_cache_service: ReviewCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> ReviewWithUserResponseList:
    return await review_cache_service.get_top_rated_movie_reviews(movie_id, size, page)


@router.get(
    "/top-newest",
    response_model=ReviewWithUserResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_top_newest_movie_reviews(
    movie_id: int,
    review_cache_service: ReviewCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> ReviewWithUserResponseList:
    return await review_cache_service.get_top_newest_movie_reviews(
        movie_id,
        size,
        page,
    )


@router.get(
    "/top-oldest",
    response_model=ReviewWithUserResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_top_oldest_movie_reviews(
    movie_id: int,
    review_cache_service: ReviewCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> ReviewWithUserResponseList:
    return await review_cache_service.get_top_oldest_movie_reviews(
        movie_id,
        size,
        page,
    )
