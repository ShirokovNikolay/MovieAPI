from fastapi import (
    APIRouter,
    Depends,
    status,
)

from dependencies.annotations.cache_services import ReviewCacheServiceDep
from dependencies.annotations.validators import PaginationPageDep, PaginationSizeDep
from dependencies.auth import get_admin_by_access_token
from dependencies.rate_limiter import check_rate_limit_auth
from schemas.review import ReviewResponse, ReviewResponseList

router = APIRouter(
    prefix="/{user_id}",
    dependencies=[
        Depends(get_admin_by_access_token),
        Depends(check_rate_limit_auth),
    ],
)


@router.get(
    "/",
    response_model=ReviewResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_user_reviews(
    user_id: int,
    review_cache_service: ReviewCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> ReviewResponseList:
    return await review_cache_service.get_user_reviews(user_id, size, page)


@router.get(
    "/movie/{movie_id}",
    response_model=ReviewResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_review_about_movie(
    user_id: int,
    movie_id: int,
    review_cache_service: ReviewCacheServiceDep,
) -> ReviewResponse:
    return await review_cache_service.get_user_review_about_movie(user_id, movie_id)
