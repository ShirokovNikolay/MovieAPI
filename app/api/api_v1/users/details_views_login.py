from typing import Annotated

from fastapi import APIRouter
from fastapi import status, Depends

from dependencies.services import get_user_service
from schemas.user import UserResponse
from services import UserService

router = APIRouter(prefix="/{login}")


@router.get(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def get_user_by_login(
    login: str,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return user_service.get_user_by_login(login)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_by_login(
    login: str,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    user_service.delete_user_by_login(login)
