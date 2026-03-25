from fastapi import APIRouter, Depends
from typing import Annotated

from dependencies import get_genre_service
from schemas.genre import GenreResponse, GenreUpdate, GenrePartialUpdate
from services import GenreService

router = APIRouter(
    prefix="/{genre_id}",
)


@router.get(
    "/",
    response_model=GenreResponse,
)
def get_genre(
    genre_id: int,
    genre_service: Annotated[GenreService, Depends(get_genre_service)],
):
    return genre_service.get_genre_by_id(genre_id)


@router.put(
    "/",
    response_model=GenreResponse,
)
def update_genre(
    genre_id: int,
    update_genre_data: GenreUpdate,
    genre_service: Annotated[GenreService, Depends(get_genre_service)],
):
    return genre_service.update_genre(genre_id, update_genre_data)


@router.patch(
    "/",
    response_model=GenreResponse,
)
def partial_update_genre(
    genre_id: int,
    partial_update_genre_data: GenrePartialUpdate,
    genre_service: Annotated[GenreService, Depends(get_genre_service)],
):
    return genre_service.partial_update_genre(genre_id, partial_update_genre_data)


@router.delete("/")
def delete_genre(
    genre_id: int,
    genre_service: Annotated[GenreService, Depends(get_genre_service)],
):
    return genre_service.delete_genre_by_id(genre_id)
