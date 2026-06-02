from fastapi import APIRouter, Depends, status
from packages.constants import S3Bucket

from core.constants import BASE_MINIO_URL
from dependencies.annotations.cache_services import GenreCacheServiceDep
from dependencies.annotations.validators import PaginationPageDep, PaginationSizeDep
from dependencies.auth import get_admin_by_access_token
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
    genre_cache_service: GenreCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
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
    genre_cache_service: GenreCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
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
    genre_cache_service: GenreCacheServiceDep,
) -> GenreResponse:
    create_genre_data.preview_url = (
        BASE_MINIO_URL
        + "/"
        + S3Bucket.genre_posters.value
        + "/"
        + create_genre_data.preview_url
    )
    return await genre_cache_service.create_genre(create_genre_data)
