from typing import Annotated

from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException,
)
from dependencies.auth import get_user_by_access_token
from dependencies.services import get_review_service, get_user_service
from schemas.review import ReviewResponseList, ReviewResponse
from services import ReviewService, UserService

router = APIRouter(
    prefix="/{user_id}",
)


@router.get(
    "/",
    response_model=ReviewResponseList,
    status_code=status.HTTP_200_OK,
)
def get_user_reviews(
    user_id: int,
    current_user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    review_service: Annotated[
        ReviewService,
        Depends(get_review_service),
    ],
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
):
    if current_user_id == user_id or user_service.is_admin(current_user_id):
        return review_service.get_user_reviews(user_id)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not allowed access to this resource",
    )


@router.get(
    "/movie/{movie_id}",
    response_model=ReviewResponse,
    status_code=status.HTTP_200_OK,
)
def get_user_review_about_movie(
    user_id: int,
    movie_id: int,
    current_user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    review_service: Annotated[
        ReviewService,
        Depends(get_review_service),
    ],
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
):
    if current_user_id == user_id or user_service.is_admin(current_user_id):
        return review_service.get_user_review_about_movie(user_id, movie_id)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not allowed access to this resource",
    )
