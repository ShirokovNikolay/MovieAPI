from typing import Annotated

from fastapi import APIRouter, Depends, Query
from starlette import status

from cache_services import FavoriteMovieCacheService
from dependencies.auth import get_admin_by_access_token, get_user_by_access_token
from dependencies.cache_services import get_favorite_movie_cache_service
from dependencies.rate_limiter import check_rate_limit_auth
from schemas.favorite_movie import FavoriteMovieResponseList

router = APIRouter(
    prefix="/users",
    dependencies=[
        Depends(check_rate_limit_auth),
    ],
)


@router.get(
    "/about-me",
    response_model=FavoriteMovieResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_current_user_favorite_movies(
    user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    favorite_movie_cache_service: Annotated[
        FavoriteMovieCacheService,
        Depends(get_favorite_movie_cache_service),
    ],
    size: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
) -> FavoriteMovieResponseList:
    return await favorite_movie_cache_service.get_favorite_movies_by_user_id(
        user_id, size, page,
    )


@router.get(
    "/{user_id}",
    response_model=FavoriteMovieResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(get_admin_by_access_token),
    ],
)
async def get_user_favorite_movies(
    user_id: int,
    favorite_movie_cache_service: Annotated[
        FavoriteMovieCacheService,
        Depends(get_favorite_movie_cache_service),
    ],
    size: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
) -> FavoriteMovieResponseList:
    return await favorite_movie_cache_service.get_favorite_movies_by_user_id(
        user_id,
        size,
        page,
    )
