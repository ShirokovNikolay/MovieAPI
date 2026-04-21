from fastapi import APIRouter, Depends, status

from dependencies.annotations.auth_annotations import AuthUserByAccessTokenDep
from dependencies.annotations.cache_services import ReviewCacheServiceDep
from dependencies.auth import (
    get_admin_by_access_token,
)
from dependencies.rate_limiter import check_rate_limit_auth
from schemas.review import (
    ReviewPartialUpdate,
    ReviewResponse,
    ReviewUpdate,
)

router = APIRouter(
    prefix="/{review_id}",
    dependencies=[
        Depends(check_rate_limit_auth),
    ],
)


@router.get(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(get_admin_by_access_token),
    ],
)
async def get_review(
    review_id: int,
    review_cache_service: ReviewCacheServiceDep,
) -> ReviewResponse:
    return await review_cache_service.get_review_by_id(review_id)


@router.put(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_200_OK,
)
async def update_review(
    user_id: AuthUserByAccessTokenDep,
    review_id: int,
    update_review_data: ReviewUpdate,
    review_cache_service: ReviewCacheServiceDep,
) -> ReviewResponse:
    return await review_cache_service.update_review(
        user_id,
        review_id,
        update_review_data,
    )


@router.patch(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_200_OK,
)
async def partial_update_review(
    user_id: AuthUserByAccessTokenDep,
    review_id: int,
    update_review_data: ReviewPartialUpdate,
    review_cache_service: ReviewCacheServiceDep,
) -> ReviewResponse:
    return await review_cache_service.partial_update_review(
        user_id,
        review_id,
        update_review_data,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_review(
    user_id: AuthUserByAccessTokenDep,
    review_id: int,
    review_cache_service: ReviewCacheServiceDep,
) -> None:
    await review_cache_service.delete_review(user_id, review_id)
