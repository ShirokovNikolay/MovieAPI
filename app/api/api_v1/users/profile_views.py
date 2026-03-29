from typing import Annotated

from fastapi import APIRouter, status, Depends
from dependencies.auth import get_current_user_id_by_access_token
from dependencies.services import get_user_service
from schemas.user import (
    UserResponse,
    UserUpdate,
    UserPartialUpdate,
)
from services import UserService

router = APIRouter(prefix="/me")


@router.get(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def get_user_profile(
    current_user_id: Annotated[
        int,
        Depends(get_current_user_id_by_access_token),
    ],
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
):
    return user_service.get_user_by_id(current_user_id)


@router.put(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def update_user_profile(
    update_data: UserUpdate,
    current_user_id: Annotated[
        int,
        Depends(get_current_user_id_by_access_token),
    ],
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
):
    return user_service.update_user(current_user_id, update_data)


@router.patch(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def partial_update_user_profile(
    update_data: UserPartialUpdate,
    current_user_id: Annotated[
        int,
        Depends(get_current_user_id_by_access_token),
    ],
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
):
    return user_service.partial_update_user(current_user_id, update_data)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_profile(
    current_user_id: Annotated[
        int,
        Depends(get_current_user_id_by_access_token),
    ],
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
):
    user_service.delete_user_by_id(current_user_id)
