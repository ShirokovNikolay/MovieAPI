from typing import Annotated

from fastapi import APIRouter, Depends, status

from dependencies import get_movie_service
from schemas.movie import MovieResponse
from services import MovieService

router = APIRouter(prefix="/{movie_name}")


@router.get(
    "/",
    response_model=MovieResponse,
    status_code=status.HTTP_200_OK,
)
def get_movie_by_name(
    movie_name: str,
    movie_service: Annotated[MovieService, Depends(get_movie_service)],
) -> MovieResponse:
    return movie_service.get_movie_by_name(movie_name)
