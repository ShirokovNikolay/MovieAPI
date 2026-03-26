from typing import Annotated

from fastapi import APIRouter, Depends, status
from dependencies import get_review_service
from schemas.review import ReviewResponse, ReviewCreate, ReviewResponseList
from services import ReviewService

router = APIRouter()


@router.get(
    "/",
    response_model=ReviewResponseList,
    status_code=status.HTTP_200_OK,
)
def get_review_list(
    review_service: Annotated[ReviewService, Depends(get_review_service)],
):
    return review_service.get_reviews()


@router.post(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_review(
    create_review_data: ReviewCreate,
    review_service: Annotated[ReviewService, Depends(get_review_service)],
    user_id: int,
):
    return review_service.create_review(user_id, create_review_data)
