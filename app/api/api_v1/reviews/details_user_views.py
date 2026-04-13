from typing import Annotated

from fastapi import (
    APIRouter,
    status,
    Depends,
    Query,
)
from dependencies.auth import get_admin_by_access_token
from dependencies.rate_limiter import check_rate_limit_auth
from dependencies.services import get_review_service
from schemas.review import ReviewResponseList, ReviewResponse
from services import ReviewService

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
    review_service: Annotated[
        ReviewService,
        Depends(get_review_service),
    ],
    size: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
):
    return await review_service.get_user_reviews(user_id, size, page)


@router.get(
    "/movie/{movie_id}",
    response_model=ReviewResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_review_about_movie(
    user_id: int,
    movie_id: int,
    review_service: Annotated[
        ReviewService,
        Depends(get_review_service),
    ],
):
    return await review_service.get_user_review_about_movie(user_id, movie_id)
