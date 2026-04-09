from typing import Annotated

from fastapi import Depends, APIRouter
from starlette import status

from dependencies.auth import get_admin_by_access_token, get_user_by_access_token
from dependencies.services import get_favorite_movie_service
from schemas.favorite_movie import FavoriteMovieList, FavoriteMovieResponse
from services.favorite_movie import FavoriteMovieService

router = APIRouter(prefix="/users")


@router.get(
    "/{user_id}",
    response_model=FavoriteMovieList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(get_admin_by_access_token),
    ],
)
async def get_user_favorite_movies(
    user_id: int,
    favorite_movie_service: Annotated[
        FavoriteMovieService,
        Depends(get_favorite_movie_service),
    ],
):
    return await favorite_movie_service.get_favorite_movies_by_user_id(user_id)


@router.get(
    "/about-me",
    response_model=FavoriteMovieList,
    status_code=status.HTTP_200_OK,
)
async def get_current_user_favorite_movies(
    user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    favorite_movie_service: Annotated[
        FavoriteMovieService,
        Depends(get_favorite_movie_service),
    ],
):
    return await favorite_movie_service.get_favorite_movies_by_user_id(user_id)


@router.get(
    "/{user_id}/movies/{movie_id}",
    response_model=FavoriteMovieResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(get_admin_by_access_token),
    ],
)
async def get_user_favorite_movie(
    user_id: int,
    movie_id: int,
    favorite_movie_service: Annotated[
        FavoriteMovieService,
        Depends(get_favorite_movie_service),
    ],
):
    return await favorite_movie_service.get_user_favorite_movie(user_id, movie_id)
