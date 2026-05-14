from fastapi import APIRouter, Depends
from starlette import status

from dependencies.annotations.cache_services import FavoriteMovieCacheServiceDep
from dependencies.annotations.security import AuthUserByAccessTokenDep
from dependencies.annotations.validators import PaginationPageDep, PaginationSizeDep
from dependencies.auth import get_admin_by_access_token
from dependencies.rate_limiter import check_rate_limit_auth, check_rate_limit_not_auth
from schemas.favorite_movie import (
    FavoriteMovieCreate,
    FavoriteMovieWithMovieResponse,
    FavoriteMovieWithMovieResponseList,
)

router = APIRouter(
    prefix="/favorite-movies",
    tags=["Favorite Movies"],
)


@router.get(
    "/{favorite_movie_id}",
    response_model=FavoriteMovieWithMovieResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_auth),
        Depends(get_admin_by_access_token),
    ],
)
async def get_favorite_movie_by_id(
    favorite_movie_id: int,
    favorite_movie_cache_service: FavoriteMovieCacheServiceDep,
) -> FavoriteMovieWithMovieResponse:
    return await favorite_movie_cache_service.get_favorite_movie_by_id(
        favorite_movie_id,
    )


@router.get(
    "/about-me",
    response_model=FavoriteMovieWithMovieResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_auth),
    ],
)
async def get_current_user_favorite_movies(
    user_id: AuthUserByAccessTokenDep,
    favorite_movie_cache_service: FavoriteMovieCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> FavoriteMovieWithMovieResponseList:
    return await favorite_movie_cache_service.get_favorite_movies_by_user_id(
        user_id,
        size,
        page,
    )


@router.get(
    "/count/{movie_id}",
    status_code=status.HTTP_200_OK,
    response_model=int,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def count_favorites_by_movie(
    movie_id: int,
    favorite_movie_cache_service: FavoriteMovieCacheServiceDep,
) -> int:
    return await favorite_movie_cache_service.count_favorites_by_movie(movie_id)


@router.post(
    "/",
    response_model=FavoriteMovieWithMovieResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(check_rate_limit_auth),
    ],
)
async def create_user_favorite_movie(
    create_favorite_movie_data: FavoriteMovieCreate,
    user_id: AuthUserByAccessTokenDep,
    favorite_movie_cache_service: FavoriteMovieCacheServiceDep,
) -> FavoriteMovieWithMovieResponse:
    return await favorite_movie_cache_service.create_user_favorite_movie(
        user_id,
        create_favorite_movie_data,
    )


@router.delete(
    "/{favorite_movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(check_rate_limit_auth),
    ],
)
async def delete_favorite_movie_by_id(
    favorite_movie_id: int,
    user_id: AuthUserByAccessTokenDep,
    favorite_movie_cache_service: FavoriteMovieCacheServiceDep,
) -> None:
    await favorite_movie_cache_service.delete_favorite_movie_by_id(
        user_id,
        favorite_movie_id,
    )


@router.delete(
    "/movies/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(check_rate_limit_auth),
    ],
)
async def delete_user_favorite_movie(
    user_id: AuthUserByAccessTokenDep,
    movie_id: int,
    favorite_movie_cache_service: FavoriteMovieCacheServiceDep,
) -> None:
    await favorite_movie_cache_service.delete_user_favorite_movie(user_id, movie_id)
