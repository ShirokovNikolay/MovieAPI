from typing import Annotated

from fastapi import APIRouter, status, Depends
from dependencies import get_review_service
from schemas.review import ReviewResponseList, ReviewResponse
from services import ReviewService

router = APIRouter(prefix="/{user_id}")


@router.get("/", response_model=ReviewResponseList, status_code=status.HTTP_200_OK)
def get_user_reviews(
    user_id: int,
    review_service: Annotated[ReviewService, Depends(get_review_service)],
) -> ReviewResponseList:
    return review_service.get_user_reviews(user_id)


@router.get(
    "/movie/{movie_id}",
    response_model=ReviewResponse,
    status_code=status.HTTP_200_OK,
)
def get_user_review_about_movie(
    user_id: int,
    movie_id: int,
    review_service: Annotated[ReviewService, Depends(get_review_service)],
):
    return review_service.get_user_review_about_movie(user_id, movie_id)
