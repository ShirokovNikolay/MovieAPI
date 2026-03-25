from typing import Annotated

from fastapi import Depends, APIRouter

from dependencies import get_genre_service
from schemas.genre import GenreResponse
from services import GenreService

router = APIRouter(
    prefix="/{genre_name}",
)


@router.get(
    "/",
    response_model=GenreResponse,
)
def get_genre_by_name(
    genre_name: str,
    genre_service: Annotated[GenreService, Depends(get_genre_service)],
):
    return genre_service.get_genre_by_name(genre_name)


@router.delete("/")
def delete_genre_by_name(
    genre_name: str,
    genre_service: Annotated[GenreService, Depends(get_genre_service)],
):
    return genre_service.delete_genre_by_name(genre_name)
