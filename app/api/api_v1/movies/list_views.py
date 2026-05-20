from datetime import datetime

from fastapi import APIRouter, Depends, status
from starlette.responses import RedirectResponse

from dependencies.annotations.cache_services import MovieCacheServiceDep
from dependencies.annotations.security import AuthUserByAccessTokenDep
from dependencies.annotations.validators import PaginationPageDep, PaginationSizeDep
from dependencies.auth import get_admin_by_access_token
from dependencies.rate_limiter import check_rate_limit_auth, check_rate_limit_not_auth
from schemas.movie import (
    MovieCreate,
    MovieFilter,
    MovieResponseList,
    MovieWithGenreResponse,
    MovieWithGenreResponseList,
)
from schemas.watch_history import WatchHistoryCreate

router = APIRouter()


@router.get(
    "/",
    response_model=MovieWithGenreResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def get_movies(
    movie_cache_service: MovieCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> MovieWithGenreResponseList:
    return await movie_cache_service.get_movies(size, page)


@router.post(
    "/watch",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    dependencies=[
        Depends(check_rate_limit_auth),
    ],
)
async def watch_movie(
    create_watch_history_data: WatchHistoryCreate,
    user_id: AuthUserByAccessTokenDep,
    movie_cache_service: MovieCacheServiceDep,
) -> RedirectResponse:
    movie = await movie_cache_service.watch_movie(user_id, create_watch_history_data)
    return RedirectResponse(url=movie.source_url)


# @router.get(
#     "/search",
#     response_model=MovieWithGenreResponseList,
#     status_code=status.HTTP_200_OK,
#     dependencies=[
#         Depends(check_rate_limit_not_auth),
#     ],
# )
# async def search_movies_by_name(
#     movie_name: str,
#     movie_cache_service: MovieCacheServiceDep,
#     size: PaginationSizeDep = 10,
#     page: PaginationPageDep = 1,
# ) -> MovieWithGenreResponseList:
#     return await movie_cache_service.search_movies_by_name(movie_name, size, page)


# Пробный view !!!
@router.post(
    "/search",
    response_model=MovieWithGenreResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def search_movies_with_filters(
    movie_filter: MovieFilter,
    movie_cache_service: MovieCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> MovieWithGenreResponseList:
    return await movie_cache_service.search_movies_with_filters(
        movie_filter,
        size,
        page,
    )


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
    response_model=MovieWithGenreResponseList,
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
) -> MovieWithGenreResponseList:
    return await movie_cache_service.get_movies_by_rating_range(
        min_rating,
        max_rating,
        size,
        page,
    )


@router.get(
    "/date-range",
    response_model=MovieWithGenreResponseList,
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
) -> MovieWithGenreResponseList:
    return await movie_cache_service.get_movies_by_release_date_range(
        release_date_start,
        release_date_end,
        size,
        page,
    )


@router.get(
    "/top-rated",
    response_model=MovieWithGenreResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def get_top_rated_movies(
    movie_cache_service: MovieCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> MovieWithGenreResponseList:
    return await movie_cache_service.get_top_rated_movies(size, page)


@router.get(
    "/top-oldest",
    response_model=MovieWithGenreResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def get_top_oldest_movies(
    movie_cache_service: MovieCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> MovieWithGenreResponseList:
    return await movie_cache_service.get_top_oldest_movies(size, page)


@router.get(
    "/top-newest",
    response_model=MovieWithGenreResponseList,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_rate_limit_not_auth),
    ],
)
async def get_top_newest_movies(
    movie_cache_service: MovieCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> MovieWithGenreResponseList:
    return await movie_cache_service.get_top_newest_movies(size, page)


@router.post(
    "/",
    response_model=MovieWithGenreResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(get_admin_by_access_token),
        Depends(check_rate_limit_auth),
    ],
)
async def create_movie(
    create_movie_data: MovieCreate,
    movie_cache_service: MovieCacheServiceDep,
) -> MovieWithGenreResponse:
    return await movie_cache_service.create_movie(create_movie_data)
