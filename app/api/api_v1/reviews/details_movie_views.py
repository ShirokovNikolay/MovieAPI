from typing import Annotated

from fastapi import APIRouter, Depends, status

from schemas.review import ReviewResponseList
from services import ReviewService
from dependencies.services import get_review_service

router = APIRouter(prefix="/{movie_id}")


@router.get(
    "/",
    response_model=ReviewResponseList,
    status_code=status.HTTP_200_OK,
)
def get_movie_reviews(
    movie_id: int,
    review_service: Annotated[
        ReviewService,
        Depends(get_review_service),
    ],
):
    return review_service.get_movie_reviews(movie_id)


@router.get(
    "/top-rated/{limit}",
    response_model=ReviewResponseList,
    status_code=status.HTTP_200_OK,
)
def get_top_rating_movie_reviews(
    movie_id: int,
    limit: int,
    review_service: Annotated[
        ReviewService,
        Depends(get_review_service),
    ],
):
    return review_service.get_top_rating_movie_reviews(movie_id, limit)


@router.get(
    "/top-newest/{limit}",
    response_model=ReviewResponseList,
    status_code=status.HTTP_200_OK,
)
def get_top_newest_movie_reviews(
    movie_id: int,
    limit: int,
    review_service: Annotated[
        ReviewService,
        Depends(get_review_service),
    ],
):
    return review_service.get_top_newest_movie_reviews(movie_id, limit)


@router.get(
    "/top-oldest/{limit}",
    response_model=ReviewResponseList,
    status_code=status.HTTP_200_OK,
)
def get_top_oldest_movie_reviews(
    movie_id: int,
    limit: int,
    review_service: Annotated[
        ReviewService,
        Depends(get_review_service),
    ],
):
    return review_service.get_top_oldest_movie_reviews(movie_id, limit)
