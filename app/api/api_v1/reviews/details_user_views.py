from fastapi import (
    APIRouter,
    Depends,
    status,
)

from dependencies.annotations.cache_services import ReviewCacheServiceDep
from dependencies.annotations.security import AuthUserByAccessTokenDep
from dependencies.annotations.validators import PaginationPageDep, PaginationSizeDep
from dependencies.rate_limiter import check_rate_limit_auth
from schemas.review import ReviewResponse, ReviewResponseList

router = APIRouter(
    prefix="/about-me",
    dependencies=[
        Depends(check_rate_limit_auth),
    ],
)


@router.get(
    "/",
    response_model=ReviewResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_current_user_reviews(
    user_id: AuthUserByAccessTokenDep,
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
async def get_current_user_review_about_movie(
    user_id: AuthUserByAccessTokenDep,
    movie_id: int,
    review_cache_service: ReviewCacheServiceDep,
) -> ReviewResponse:
    return await review_cache_service.get_user_review_about_movie(user_id, movie_id)
