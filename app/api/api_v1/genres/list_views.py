from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies import get_genre_service
from schemas.genre import GenreResponseList, GenreResponse, GenreCreate
from services import GenreService

router = APIRouter()


@router.get(
    "/",
    response_model=GenreResponseList,
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
)
def create_genre(
    create_genre_data: GenreCreate,
    genre_service: Annotated[GenreService, Depends(get_genre_service)],
):
    return genre_service.create_genre(create_genre_data)
