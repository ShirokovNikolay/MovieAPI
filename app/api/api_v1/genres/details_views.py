from fastapi import APIRouter, Depends, status
from packages.constants import S3Bucket

from core.constants import BASE_MINIO_URL
from dependencies.annotations.cache_services import GenreCacheServiceDep
from dependencies.auth import get_admin_by_access_token
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
    genre_cache_service: GenreCacheServiceDep,
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
    genre_cache_service: GenreCacheServiceDep,
) -> GenreResponse:
    update_genre_data.preview_url = (
        BASE_MINIO_URL
        + "/"
        + S3Bucket.genre_posters.value
        + "/"
        + update_genre_data.preview_url
    )
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
    genre_cache_service: GenreCacheServiceDep,
) -> GenreResponse:
    if partial_update_genre_data.preview_url is not None:
        partial_update_genre_data.preview_url = (
            BASE_MINIO_URL
            + "/"
            + S3Bucket.genre_posters.value
            + "/"
            + partial_update_genre_data.preview_url
        )
    return await genre_cache_service.partial_update_genre(
        genre_id,
        partial_update_genre_data,
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
    genre_cache_service: GenreCacheServiceDep,
) -> None:
    return await genre_cache_service.delete_genre_by_id(genre_id)
