from fastapi import APIRouter, Depends, status

from dependencies.annotations.cache_services import MovieCacheServiceDep
from dependencies.auth import get_admin_by_access_token
from dependencies.rate_limiter import check_rate_limit_auth, check_rate_limit_not_auth
from schemas.movie import (
    MoviePartialUpdate,
    MovieUpdate,
    MovieWithGenreResponse,
)

router = APIRouter(
    prefix="/{movie_id}",
)


@router.get(
    "/",
    response_model=MovieWithGenreResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def get_movie(
    movie_id: int,
    movie_cache_service: MovieCacheServiceDep,
) -> MovieWithGenreResponse:
    return await movie_cache_service.get_movie_by_id(movie_id)


@router.put(
    "/",
    response_model=MovieWithGenreResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(get_admin_by_access_token),
        Depends(check_rate_limit_auth),
    ],
)
async def update_movie(
    movie_id: int,
    update_movie_data: MovieUpdate,
    movie_cache_service: MovieCacheServiceDep,
) -> MovieWithGenreResponse:
    return await movie_cache_service.update_movie(movie_id, update_movie_data)


@router.patch(
    "/",
    response_model=MovieWithGenreResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(get_admin_by_access_token),
        Depends(check_rate_limit_auth),
    ],
)
async def partial_update_movie(
    movie_id: int,
    update_movie_data: MoviePartialUpdate,
    movie_cache_service: MovieCacheServiceDep,
) -> MovieWithGenreResponse:
    return await movie_cache_service.partial_update_movie(movie_id, update_movie_data)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(get_admin_by_access_token),
        Depends(check_rate_limit_auth),
    ],
)
async def delete_movie(
    movie_id: int,
    movie_cache_service: MovieCacheServiceDep,
) -> None:
    await movie_cache_service.delete_movie_by_id(movie_id)
