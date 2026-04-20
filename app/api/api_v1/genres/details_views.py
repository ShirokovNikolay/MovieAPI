from typing import Annotated

from fastapi import APIRouter, Depends, status

from cache_services import GenreCacheService
from dependencies.auth import get_admin_by_access_token
from dependencies.cache_services import get_genre_cache_service
from dependencies.rate_limiter import check_rate_limit_auth, check_rate_limit_not_auth
from schemas.genre import GenrePartialUpdate, GenreResponse, GenreUpdate

router = APIRouter(
    prefix="/{genre_id}",
)


@router.get(
    "/",
    response_model=GenreResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def get_genre(
    genre_id: int,
    genre_cache_service: Annotated[
        GenreCacheService,
        Depends(get_genre_cache_service),
    ],
) -> GenreResponse:
    return await genre_cache_service.get_genre_by_id(genre_id)


@router.put(
    "/",
    response_model=GenreResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(get_admin_by_access_token),
        Depends(check_rate_limit_auth),
    ],
)
async def update_genre(
    genre_id: int,
    update_genre_data: GenreUpdate,
    genre_cache_service: Annotated[
        GenreCacheService,
        Depends(get_genre_cache_service),
    ],
) -> GenreResponse:
    return await genre_cache_service.update_genre(genre_id, update_genre_data)


@router.patch(
    "/",
    response_model=GenreResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(get_admin_by_access_token),
        Depends(check_rate_limit_auth),
    ],
)
async def partial_update_genre(
    genre_id: int,
    partial_update_genre_data: GenrePartialUpdate,
    genre_cache_service: Annotated[
        GenreCacheService,
        Depends(get_genre_cache_service),
    ],
) -> GenreResponse:
    return await genre_cache_service.partial_update_genre(
        genre_id, partial_update_genre_data,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(get_admin_by_access_token),
        Depends(check_rate_limit_auth),
    ],
)
async def delete_genre(
    genre_id: int,
    genre_cache_service: Annotated[
        GenreCacheService,
        Depends(get_genre_cache_service),
    ],
) -> None:
    return await genre_cache_service.delete_genre_by_id(genre_id)
