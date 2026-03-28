from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status

from dependencies.services import get_movie_service
from schemas.movie import MovieResponseList, MovieCreate, MovieResponse

from services import MovieService

router = APIRouter()


@router.get(
    "/",
    response_model=MovieResponseList,
    status_code=status.HTTP_200_OK,
)
def get_movies(
    movie_service: Annotated[MovieService, Depends(get_movie_service)],
):
    return movie_service.get_movies()


@router.get(
    "/genre/{genre_id}",
    response_model=MovieResponseList,
    status_code=status.HTTP_200_OK,
)
def get_movies_by_genre_id(
    genre_id: int,
    movie_service: Annotated[MovieService, Depends(get_movie_service)],
):
    return movie_service.get_movies_by_genre_id(genre_id)


@router.get(
    "/genre-name/{genre_name}",
    response_model=MovieResponseList,
    status_code=status.HTTP_200_OK,
)
def get_movies_by_genre_name(
    genre_name: str,
    movie_service: Annotated[MovieService, Depends(get_movie_service)],
):
    return movie_service.get_movies_by_genre_name(genre_name)


@router.get(
    "/rating-range",
    response_model=MovieResponseList,
    status_code=status.HTTP_200_OK,
)
def get_movies_by_rating_range(
    min_rating: int,
    max_rating: int,
    movie_service: Annotated[MovieService, Depends(get_movie_service)],
):
    return movie_service.get_movies_by_rating_range(min_rating, max_rating)


@router.get("/date-range")
def get_movies_by_release_date_range(
    release_date_start: datetime,
    release_date_end: datetime,
    movie_service: Annotated[MovieService, Depends(get_movie_service)],
):
    return movie_service.get_movies_by_release_date_range(
        release_date_start, release_date_end
    )


@router.get(
    "/year/{year}",
    response_model=MovieResponseList,
    status_code=status.HTTP_200_OK,
)
def get_movies_by_year(
    year: int,
    movie_service: Annotated[MovieService, Depends(get_movie_service)],
):
    return movie_service.get_movies_by_year(year)


@router.get(
    "/top-rated/{limit}",
    response_model=MovieResponseList,
    status_code=status.HTTP_200_OK,
)
def get_top_rated_movies(
    limit: int,
    movie_service: Annotated[MovieService, Depends(get_movie_service)],
) -> MovieResponseList:
    return movie_service.get_top_rated_movies(limit)


@router.get(
    "/top-oldest/{limit}",
    response_model=MovieResponseList,
    status_code=status.HTTP_200_OK,
)
def get_top_oldest_movies(
    limit: int,
    movie_service: Annotated[MovieService, Depends(get_movie_service)],
) -> MovieResponseList:
    return movie_service.get_top_oldest_movies(limit)


@router.get(
    "/top-newest/{limit}",
    response_model=MovieResponseList,
    status_code=status.HTTP_200_OK,
)
def get_top_newest_movies(
    limit: int,
    movie_service: Annotated[MovieService, Depends(get_movie_service)],
) -> MovieResponseList:
    return movie_service.get_top_newest_movies(limit)


@router.post(
    "/",
    response_model=MovieResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    create_movie_data: MovieCreate,
    movie_service: Annotated[MovieService, Depends(get_movie_service)],
):
    return movie_service.create_movie(create_movie_data)
