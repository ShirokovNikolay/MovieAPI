from typing import Annotated

from fastapi import APIRouter, status, Depends
from dependencies.auth import get_own_reviews, get_own_review_about_movie
from schemas.review import ReviewResponseList, ReviewResponse

router = APIRouter(
    prefix="/{user_id}",
)


@router.get(
    "/",
    response_model=ReviewResponseList,
    status_code=status.HTTP_200_OK,
)
def get_user_reviews(
    reviews: Annotated[
        ReviewResponseList,
        Depends(get_own_reviews),
    ],
):
    return reviews


@router.get(
    "/movie/{movie_id}",
    response_model=ReviewResponse,
    status_code=status.HTTP_200_OK,
)
def get_user_review_about_movie(
    review: Annotated[
        ReviewResponseList,
        Depends(get_own_review_about_movie),
    ],
):
    return review
