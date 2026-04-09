from typing import Annotated

from fastapi import APIRouter, Depends, status

from dependencies.auth import get_admin_by_access_token, get_user_by_access_token
from api.api_v1.favorite_movies.details_user_views import get_favorite_movie_service
from schemas.favorite_movie import (
    FavoriteMovieResponse,
    FavoriteMovieCreate,
)
from services.favorite_movie import FavoriteMovieService

router = APIRouter()


@router.get(
    "/{favorite_movie_id}",
    response_model=FavoriteMovieResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(get_admin_by_access_token),
    ],
)
async def get_favorite_movie_by_id(
    favorite_movie_id: int,
    favorite_movie_service: Annotated[
        FavoriteMovieService,
        Depends(get_favorite_movie_service),
    ],
):
    return await favorite_movie_service.get_favorite_movie_by_id(favorite_movie_id)


@router.get(
    "/count/{movie_id}",
    status_code=status.HTTP_200_OK,
)
async def count_favorites_by_movie(
    movie_id: int,
    favorite_movie_service: Annotated[
        FavoriteMovieService,
        Depends(get_favorite_movie_service),
    ],
):
    return await favorite_movie_service.count_favorites_by_movie(movie_id)


@router.post(
    "/",
    response_model=FavoriteMovieResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_favorite_movie(
    create_favorite_movie_data: FavoriteMovieCreate,
    user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    favorite_movie_service: Annotated[
        FavoriteMovieService,
        Depends(get_favorite_movie_service),
    ],
):
    return await favorite_movie_service.create_user_favorite_movie(
        user_id,
        create_favorite_movie_data,
    )


@router.delete(
    "/{favorite_movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(get_admin_by_access_token),
    ],
)
async def delete_favorite_movie_by_id(
    favorite_movie_id: int,
    favorite_movie_service: Annotated[
        FavoriteMovieService,
        Depends(get_favorite_movie_service),
    ],
):
    await favorite_movie_service.delete_favorite_movie_by_id(favorite_movie_id)


@router.delete(
    "/movies/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_favorite_movie(
    user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    movie_id: int,
    favorite_movie_service: Annotated[
        FavoriteMovieService,
        Depends(get_favorite_movie_service),
    ],
):
    await favorite_movie_service.delete_user_favorite_movie(user_id, movie_id)
