from fastapi import APIRouter, Depends, status

from dependencies.annotations.auth_annotations import AuthUserByAccessTokenDep
from dependencies.annotations.cache_services import ReviewCacheServiceDep
from dependencies.annotations.validators import PaginationPageDep, PaginationSizeDep
from dependencies.auth import (
    get_admin_by_access_token,
)
from dependencies.rate_limiter import check_rate_limit_auth
from schemas.review import (
    ReviewCreate,
    ReviewResponse,
    ReviewResponseList,
)

router = APIRouter(
    dependencies=[
        Depends(check_rate_limit_auth),
    ],
)


@router.get(
    "/",
    response_model=ReviewResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(get_admin_by_access_token),
    ],
)
async def get_review_list(
    review_cache_service: ReviewCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> ReviewResponseList:
    return await review_cache_service.get_reviews(size, page)


@router.post(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    create_review_data: ReviewCreate,
    user_id: AuthUserByAccessTokenDep,
    review_cache_service: ReviewCacheServiceDep,
) -> ReviewResponse:
    return await review_cache_service.create_review(user_id, create_review_data)
