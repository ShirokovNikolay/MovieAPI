from fastapi import APIRouter, Depends
from starlette import status

from dependencies.annotations.cache_services import FavoriteMovieCacheServiceDep
from dependencies.annotations.security import AuthUserByAccessTokenDep
from dependencies.annotations.validators import PaginationPageDep, PaginationSizeDep
from dependencies.auth import get_admin_by_access_token
from dependencies.rate_limiter import check_rate_limit_auth
from schemas.favorite_movie import FavoriteMovieWithMovieResponseList

router = APIRouter(
    prefix="/users",
    dependencies=[
        Depends(check_rate_limit_auth),
    ],
)


@router.get(
    "/about-me",
    response_model=FavoriteMovieWithMovieResponseList,
    status_code=status.HTTP_200_OK,
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
    "/{user_id}",
    response_model=FavoriteMovieWithMovieResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(get_admin_by_access_token),
    ],
)
async def get_user_favorite_movies(
    user_id: int,
    favorite_movie_cache_service: FavoriteMovieCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> FavoriteMovieWithMovieResponseList:
    return await favorite_movie_cache_service.get_favorite_movies_by_user_id(
        user_id,
        size,
        page,
    )
