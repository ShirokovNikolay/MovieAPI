from datetime import datetime
from core.security.cache_utils import create_cache_key
from redis_cache import CacheService

from schemas.movie import (
    MovieResponse,
    MovieResponseList,
    MovieCreate,
    MovieUpdate,
    MoviePartialUpdate,
)
from schemas.watch_history import WatchHistoryCreate

from services import MovieService


class MovieCacheService:
    def __init__(
        self,
        movie_service: MovieService,
        cache_service_for_movie: CacheService,
        cache_service_for_watch_history: CacheService,
    ):
        self.movie_service = movie_service
        self.cache_service_for_movie = cache_service_for_movie
        self.cache_service_for_watch_history = cache_service_for_watch_history

    async def get_movie_by_id(self, movie_id: int) -> MovieResponse:
        key = create_cache_key("movie", movie_id=movie_id)
        cached_movie_response = await self.cache_service_for_movie.get(
            key, MovieResponse
        )
        if cached_movie_response is not None:
            return cached_movie_response

        movie_response = await self.movie_service.get_movie_by_id(movie_id)
        await self.cache_service_for_movie.set(key, movie_response, ttl=60)
        return movie_response

    async def get_movies(
        self,
        size: int = 10,
        page: int = 1,
    ) -> MovieResponseList:
        key = create_cache_key("movies", size=size, page=page)
        cached_movies_response = await self.cache_service_for_movie.get(
            key, MovieResponseList
        )
        if cached_movies_response is not None:
            return cached_movies_response

        movies_response = await self.movie_service.get_movies(size, page)
        await self.cache_service_for_movie.set(key, movies_response, ttl=60)
        return movies_response

    async def get_movies_by_genre_id(
        self,
        genre_id: int,
        size: int = 10,
        page: int = 1,
    ) -> MovieResponseList:
        key = create_cache_key(
            "movies",
            genre_id=genre_id,
            size=size,
            page=page,
        )
        cached_movies_response = await self.cache_service_for_movie.get(
            key, MovieResponseList
        )
        if cached_movies_response is not None:
            return cached_movies_response

        movies_response = await self.movie_service.get_movies_by_genre_id(
            genre_id, size, page
        )
        await self.cache_service_for_movie.set(key, movies_response, ttl=1800)
        return movies_response

    async def search_movies_by_name(
        self,
        name: str,
        size: int = 10,
        page: int = 1,
    ) -> MovieResponseList:
        key = create_cache_key(
            "movies",
            name=name,
            size=size,
            page=page,
        )
        cached_movies_response = await self.cache_service_for_movie.get(
            key, MovieResponseList
        )
        if cached_movies_response is not None:
            return cached_movies_response

        movies_response = await self.movie_service.search_movies_by_name(
            name, size, page
        )
        await self.cache_service_for_movie.set(key, movies_response, ttl=60)
        return movies_response

    async def get_movies_by_rating_range(
        self,
        min_rating: int,
        max_rating: int,
        size: int = 10,
        page: int = 1,
    ) -> MovieResponseList:
        key = create_cache_key(
            "movies",
            min_rating=min_rating,
            max_rating=max_rating,
            size=size,
            page=page,
        )
        cached_movies_response = await self.cache_service_for_movie.get(
            key, MovieResponseList
        )
        if cached_movies_response is not None:
            return cached_movies_response

        movies_response = await self.movie_service.get_movies_by_rating_range(
            min_rating,
            max_rating,
            size,
            page,
        )
        await self.cache_service_for_movie.set(key, movies_response, ttl=60)
        return movies_response

    async def get_movies_by_year(
        self,
        year: int,
        size: int = 10,
        page: int = 1,
    ) -> MovieResponseList:
        key = create_cache_key("movies", year=year, size=size, page=page)
        cached_movies_response = await self.cache_service_for_movie.get(
            key, MovieResponseList
        )
        if cached_movies_response is not None:
            return cached_movies_response

        movies_response = await self.movie_service.get_movies_by_year(year, size, page)
        await self.cache_service_for_movie.set(key, movies_response, ttl=60)
        return movies_response

    async def get_movies_by_release_date_range(
        self,
        release_date_start: datetime,
        release_date_end: datetime,
        size: int = 10,
        page: int = 1,
    ) -> MovieResponseList:
        key = create_cache_key(
            "movies",
            release_date_start=release_date_start,
            release_date_end=release_date_end,
            size=size,
            page=page,
        )
        cached_movies_response = await self.cache_service_for_movie.get(
            key, MovieResponseList
        )
        if cached_movies_response is not None:
            return cached_movies_response

        movies_response = await self.movie_service.get_movies_by_release_date_range(
            release_date_start,
            release_date_end,
            size,
            page,
        )
        await self.cache_service_for_movie.set(key, movies_response, ttl=60)
        return movies_response

    async def get_top_rated_movies(self, limit: int) -> MovieResponseList:
        key = create_cache_key("movies:top-rated", limit=limit)
        cached_movies_response = await self.cache_service_for_movie.get(
            key, MovieResponseList
        )
        if cached_movies_response is not None:
            return cached_movies_response

        movies_response = await self.movie_service.get_top_rated_movies(limit)
        await self.cache_service_for_movie.set(key, movies_response, ttl=60)
        return movies_response

    async def get_top_newest_movies(self, limit: int) -> MovieResponseList:
        key = create_cache_key("movies:top-newest", limit=limit)
        cached_movies_response = await self.cache_service_for_movie.get(
            key, MovieResponseList
        )
        if cached_movies_response is not None:
            return cached_movies_response

        movies_response = await self.movie_service.get_top_newest_movies(limit)
        await self.cache_service_for_movie.set(key, movies_response, ttl=60)
        return movies_response

    async def get_top_oldest_movies(self, limit: int) -> MovieResponseList:
        key = create_cache_key("movies:top-oldest", limit=limit)
        cached_movies_response = await self.cache_service_for_movie.get(
            key, MovieResponseList
        )
        if cached_movies_response is not None:
            return cached_movies_response

        movies_response = await self.movie_service.get_top_oldest_movies(limit)
        await self.cache_service_for_movie.set(key, movies_response, ttl=60)
        return movies_response

    async def watch_movie(
        self,
        user_id: int,
        create_watch_history_data: WatchHistoryCreate,
    ) -> MovieResponse:
        movie_response = await self.movie_service.watch_movie(
            user_id, create_watch_history_data
        )
        key = create_cache_key("watch_history")
        pattern = key + "*"
        await self.cache_service_for_watch_history.delete_by_pattern(pattern)
        return movie_response

    async def create_movie(self, create_movie_data: MovieCreate) -> MovieResponse:
        movie_response = await self.movie_service.create_movie(create_movie_data)
        key = create_cache_key("movie")
        pattern = key + "*"
        await self.cache_service_for_movie.delete_by_pattern(pattern)
        return movie_response

    async def update_movie(
        self,
        movie_id: int,
        update_movie_data: MovieUpdate,
    ) -> MovieResponse:
        movie_response = await self.movie_service.update_movie(
            movie_id, update_movie_data
        )
        key = create_cache_key("movie")
        pattern = key + "*"
        await self.cache_service_for_movie.delete_by_pattern(pattern)
        return movie_response

    async def partial_update_movie(
        self,
        movie_id: int,
        update_movie_data: MoviePartialUpdate,
    ) -> MovieResponse:
        movie_response = await self.movie_service.partial_update_movie(
            movie_id, update_movie_data
        )
        key = create_cache_key("movie")
        pattern = key + "*"
        await self.cache_service_for_movie.delete_by_pattern(pattern)
        return movie_response

    async def delete_movie_by_id(self, movie_id: int) -> None:
        await self.movie_service.delete_movie_by_id(movie_id)
        key = create_cache_key("movie")
        pattern = key + "*"
        await self.cache_service_for_movie.delete_by_pattern(pattern)
