from typing import Annotated

from fastapi import APIRouter, status, Depends

from dependencies.auth import get_current_user_id_by_access_token
from schemas.review import ReviewResponse, ReviewUpdate, ReviewPartialUpdate
from dependencies.services import get_review_service
from services import ReviewService

router = APIRouter(prefix="/{review_id}")


@router.get(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_200_OK,
)
def get_review(
    review_id: int,
    review_service: Annotated[
        ReviewService,
        Depends(get_review_service),
    ],
):
    return review_service.get_review_by_id(review_id)


@router.put(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_200_OK,
)
def update_review(
    current_user_id: Annotated[
        int,
        Depends(get_current_user_id_by_access_token),
    ],
    review_id: int,
    update_review_data: ReviewUpdate,
    review_service: Annotated[
        ReviewService,
        Depends(get_review_service),
    ],
):
    return review_service.update_review(
        current_user_id,
        review_id,
        update_review_data,
    )


@router.patch(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_200_OK,
)
def partial_update_review(
    current_user_id: Annotated[
        int,
        Depends(get_current_user_id_by_access_token),
    ],
    review_id: int,
    update_review_data: ReviewPartialUpdate,
    review_service: Annotated[
        ReviewService,
        Depends(get_review_service),
    ],
):
    return review_service.partial_update_review(
        current_user_id,
        review_id,
        update_review_data,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_review(
    user_id: int,
    review_id: int,
    review_service: Annotated[
        ReviewService,
        Depends(get_review_service),
    ],
):
    review_service.delete_review(user_id, review_id)
