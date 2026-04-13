from typing import Annotated

from fastapi import APIRouter, Depends, status, Query

from dependencies.auth import (
    get_admin_by_access_token,
    get_user_by_access_token,
)
from dependencies.rate_limiter import check_rate_limit_auth
from dependencies.services import get_review_service
from schemas.review import (
    ReviewResponse,
    ReviewCreate,
    ReviewResponseList,
)
from services import ReviewService

router = APIRouter(
    dependencies=[
        Depends(check_rate_limit_auth),
    ]
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
    review_service: Annotated[
        ReviewService,
        Depends(get_review_service),
    ],
    size: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
):
    return await review_service.get_reviews(size, page)


@router.post(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    create_review_data: ReviewCreate,
    current_user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    review_service: Annotated[
        ReviewService,
        Depends(get_review_service),
    ],
):
    return await review_service.create_review(current_user_id, create_review_data)
