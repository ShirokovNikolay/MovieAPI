from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from cache_services import GenreCacheService
from dependencies.auth import get_admin_by_access_token
from dependencies.cache_services import get_genre_cache_service
from dependencies.rate_limiter import check_rate_limit_auth, check_rate_limit_not_auth
from schemas.genre import GenreCreate, GenreResponse, GenreResponseList

router = APIRouter()


@router.get(
    "/",
    response_model=GenreResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def get_genres(
    genre_cache_service: Annotated[
        GenreCacheService,
        Depends(get_genre_cache_service),
    ],
    size: Annotated[
        int,
        Query(ge=1),
    ] = 10,
    page: Annotated[
        int,
        Query(ge=1),
    ] = 1,
) -> GenreResponseList:
    return await genre_cache_service.get_all_genres(size, page)


@router.get(
    "/search",
    response_model=GenreResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def search_genres_by_name(
    genre_name: str,
    genre_cache_service: Annotated[
        GenreCacheService,
        Depends(get_genre_cache_service),
    ],
    size: Annotated[
        int,
        Query(ge=1),
    ] = 10,
    page: Annotated[
        int,
        Query(ge=1),
    ] = 1,
) -> GenreResponseList:
    return await genre_cache_service.search_genres_by_name(genre_name, size, page)


@router.post(
    "/",
    response_model=GenreResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(get_admin_by_access_token),
        Depends(check_rate_limit_auth),
    ],
)
async def create_genre(
    create_genre_data: GenreCreate,
    genre_cache_service: Annotated[
        GenreCacheService,
        Depends(get_genre_cache_service),
    ],
) -> GenreResponse:
    return await genre_cache_service.create_genre(create_genre_data)
