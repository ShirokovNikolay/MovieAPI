from typing import Annotated

from fastapi import APIRouter, status, Depends

from cache_services import ReviewCacheService
from dependencies.auth import (
    get_user_by_access_token,
    get_admin_by_access_token,
)
from dependencies.cache_services import get_review_cache_service
from dependencies.rate_limiter import check_rate_limit_auth
from schemas.review import (
    ReviewResponse,
    ReviewUpdate,
    ReviewPartialUpdate,
)
from dependencies.services import get_review_service
from services import ReviewService

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
    review_cache_service: Annotated[
        ReviewCacheService,
        Depends(get_review_cache_service),
    ],
) -> ReviewResponse:
    return await review_cache_service.get_review_by_id(review_id)


@router.put(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_200_OK,
)
async def update_review(
    current_user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    review_id: int,
    update_review_data: ReviewUpdate,
    review_cache_service: Annotated[
        ReviewCacheService,
        Depends(get_review_cache_service),
    ],
) -> ReviewResponse:
    return await review_cache_service.update_review(
        current_user_id,
        review_id,
        update_review_data,
    )


@router.patch(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_200_OK,
)
async def partial_update_review(
    current_user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    review_id: int,
    update_review_data: ReviewPartialUpdate,
    review_cache_service: Annotated[
        ReviewCacheService,
        Depends(get_review_cache_service),
    ],
) -> ReviewResponse:
    return await review_cache_service.partial_update_review(
        current_user_id,
        review_id,
        update_review_data,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_review(
    current_user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    review_id: int,
    review_cache_service: Annotated[
        ReviewCacheService,
        Depends(get_review_cache_service),
    ],
) -> None:
    await review_cache_service.delete_review(current_user_id, review_id)
