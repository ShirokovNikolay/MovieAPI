from typing import Annotated

from fastapi import APIRouter, Depends, status

from dependencies import get_genre_service
from schemas.genre import GenreResponseList, GenreResponse, GenreCreate
from services import GenreService

router = APIRouter()


@router.get(
    "/",
    response_model=GenreResponseList,
    status_code=status.HTTP_200_OK,
)
def get_genres(
    genre_service: Annotated[
        GenreService,
        Depends(get_genre_service),
    ],
):
    return genre_service.get_all_genres()


@router.post(
    "/",
    response_model=GenreResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_genre(
    create_genre_data: GenreCreate,
    genre_service: Annotated[GenreService, Depends(get_genre_service)],
):
    return genre_service.create_genre(create_genre_data)
