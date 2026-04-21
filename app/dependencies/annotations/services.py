from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.services import (
    get_db,
    get_favorite_movie_service,
    get_genre_service,
    get_movie_service,
    get_review_service,
    get_user_service,
    get_watch_history_service,
)
from services import (
    FavoriteMovieService,
    GenreService,
    MovieService,
    ReviewService,
    UserService,
    WatchHistoryService,
)

DbSessionDep = Annotated[
    AsyncSession,
    Depends(
        get_db,
    ),
]

GenreServiceDep = Annotated[
    GenreService,
    Depends(
        get_genre_service,
    ),
]

MovieServiceDep = Annotated[
    MovieService,
    Depends(
        get_movie_service,
    ),
]

FavoriteMovieServiceDep = Annotated[
    FavoriteMovieService,
    Depends(
        get_favorite_movie_service,
    ),
]

ReviewServiceDep = Annotated[
    ReviewService,
    Depends(
        get_review_service,
    ),
]

UserServiceDep = Annotated[
    UserService,
    Depends(
        get_user_service,
    ),
]

WatchHistoryServiceDep = Annotated[
    WatchHistoryService,
    Depends(
        get_watch_history_service,
    ),
]
