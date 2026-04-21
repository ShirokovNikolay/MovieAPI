from datetime import datetime

from fastapi import APIRouter, Depends, status

from dependencies.annotations.cache_services import MovieCacheServiceDep
from dependencies.annotations.validators import PaginationPageDep, PaginationSizeDep
from dependencies.auth import get_admin_by_access_token
from dependencies.rate_limiter import check_rate_limit_auth, check_rate_limit_not_auth
from schemas.movie import MovieCreate, MovieResponse, MovieResponseList

router = APIRouter()


@router.get(
    "/",
    response_model=MovieResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def get_movies(
    movie_cache_service: MovieCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> MovieResponseList:
    return await movie_cache_service.get_movies(size, page)


@router.get(
    "/search",
    response_model=MovieResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def search_movies_by_name(
    movie_name: str,
    movie_cache_service: MovieCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> MovieResponseList:
    return await movie_cache_service.search_movies_by_name(movie_name, size, page)


@router.get(
    "/genre/{genre_id}",
    response_model=MovieResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def get_movies_by_genre_id(
    genre_id: int,
    movie_cache_service: MovieCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> MovieResponseList:
    return await movie_cache_service.get_movies_by_genre_id(genre_id, size, page)


@router.get(
    "/rating-range",
    response_model=MovieResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def get_movies_by_rating_range(
    min_rating: int,
    max_rating: int,
    movie_cache_service: MovieCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> MovieResponseList:
    return await movie_cache_service.get_movies_by_rating_range(
        min_rating,
        max_rating,
        size,
        page,
    )


@router.get(
    "/date-range",
    response_model=MovieResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def get_movies_by_release_date_range(
    release_date_start: datetime,
    release_date_end: datetime,
    movie_cache_service: MovieCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> MovieResponseList:
    return await movie_cache_service.get_movies_by_release_date_range(
        release_date_start,
        release_date_end,
        size,
        page,
    )


@router.get(
    "/year/{year}",
    response_model=MovieResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def get_movies_by_year(
    year: int,
    movie_cache_service: MovieCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> MovieResponseList:
    return await movie_cache_service.get_movies_by_year(
        year,
        size,
        page,
    )


@router.get(
    "/top-rated/{limit}",
    response_model=MovieResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def get_top_rated_movies(
    limit: int,
    movie_cache_service: MovieCacheServiceDep,
) -> MovieResponseList:
    return await movie_cache_service.get_top_rated_movies(limit)


@router.get(
    "/top-oldest/{limit}",
    response_model=MovieResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def get_top_oldest_movies(
    limit: int,
    movie_cache_service: MovieCacheServiceDep,
) -> MovieResponseList:
    return await movie_cache_service.get_top_oldest_movies(limit)


@router.get(
    "/top-newest/{limit}",
    response_model=MovieResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def get_top_newest_movies(
    limit: int,
    movie_cache_service: MovieCacheServiceDep,
) -> MovieResponseList:
    return await movie_cache_service.get_top_newest_movies(limit)


@router.post(
    "/",
    response_model=MovieResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(get_admin_by_access_token),
        Depends(check_rate_limit_auth),
    ],
)
async def create_movie(
    create_movie_data: MovieCreate,
    movie_cache_service: MovieCacheServiceDep,
) -> MovieResponse:
    return await movie_cache_service.create_movie(create_movie_data)
