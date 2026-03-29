from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status
from fastapi.responses import RedirectResponse

from dependencies.services import get_movie_service
from dependencies.auth import get_current_user_id_by_access_token
from schemas.movie import (
    MovieResponse,
    MovieUpdate,
    MoviePartialUpdate,
)
from services import MovieService

router = APIRouter(
    prefix="/{movie_id}",
)


@router.get(
    "/watch",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
def watch_movie(
    movie_id: int,
    movie_service: Annotated[
        MovieService,
        Depends(get_movie_service),
    ],
    _=Depends(get_current_user_id_by_access_token),
):
    movie = movie_service.get_movie_by_id(movie_id)
    return RedirectResponse(url=movie.source_url)


@router.get(
    "/",
    response_model=MovieResponse,
    status_code=status.HTTP_200_OK,
)
def get_movie(
    movie_id: int,
    movie_service: Annotated[
        MovieService,
        Depends(get_movie_service),
    ],
) -> MovieResponse:
    return movie_service.get_movie_by_id(movie_id)


@router.put(
    "/",
    response_model=MovieResponse,
    status_code=status.HTTP_200_OK,
)
def update_movie(
    movie_id: int,
    update_movie_data: MovieUpdate,
    movie_service: Annotated[
        MovieService,
        Depends(get_movie_service),
    ],
):
    return movie_service.update_movie(movie_id, update_movie_data)


@router.patch(
    "/",
    response_model=MovieResponse,
    status_code=status.HTTP_200_OK,
)
def partial_update_movie(
    movie_id: int,
    update_movie_data: MoviePartialUpdate,
    movie_service: Annotated[
        MovieService,
        Depends(get_movie_service),
    ],
):
    return movie_service.partial_update_movie(movie_id, update_movie_data)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(
    movie_id: int,
    movie_service: Annotated[
        MovieService,
        Depends(get_movie_service),
    ],
):
    movie_service.delete_movie_by_id(movie_id)
