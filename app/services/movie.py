from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import status

from repositories import MovieRepository
from schemas.movie import (
    MovieResponse,
    MovieResponseList,
    MovieCreate,
    MovieUpdate,
    MoviePartialUpdate,
)


class MovieService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.movie_repository = MovieRepository(session)

    def get_movie_by_id(self, movie_id: int) -> MovieResponse:
        movie = self.movie_repository.get_movie_by_id(movie_id)
        if movie is not None:
            return MovieResponse.model_validate(movie)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with {movie_id=} not found",
        )

    def get_movie_by_name(self, movie_name: str) -> MovieResponse:
        movie = self.movie_repository.get_movie_by_name(movie_name)
        if movie is not None:
            return MovieResponse.model_validate(movie)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie {movie_name=} not found",
        )

    def get_movies_by_genre_id(self, genre_id: int) -> MovieResponseList:
        movies = [
            MovieResponse.model_validate(movie)
            for movie in self.movie_repository.get_movies_by_genre_id(genre_id)
        ]
        return MovieResponseList(movie_list=movies)

    def get_movies_by_genre_name(self, genre_name: str) -> MovieResponseList:
        movies = [
            MovieResponse.model_validate(movie)
            for movie in self.movie_repository.get_movies_by_genre_name(genre_name)
        ]
        return MovieResponseList(movie_list=movies)

    def get_movies_by_rating_range(
        self,
        min_rating: int,
        max_rating: int,
    ) -> MovieResponseList:
        movies = [
            MovieResponse.model_validate(movie)
            for movie in self.movie_repository.get_movies_by_rating_range(
                min_rating,
                max_rating,
            )
        ]
        return MovieResponseList(movie_list=movies)

    def get_movies_by_year(self, year: int) -> MovieResponseList:
        movies = [
            MovieResponse.model_validate(movie)
            for movie in self.movie_repository.get_movies_by_year(year)
        ]
        return MovieResponseList(movie_list=movies)

    def get_movies_by_release_date(
        self,
        release_date_start: datetime,
        release_date_end: datetime,
    ) -> MovieResponseList:
        movies = [
            MovieResponse.model_validate(movie)
            for movie in self.movie_repository.get_movies_by_release_date(
                release_date_start,
                release_date_end,
            )
        ]
        return MovieResponseList(movie_list=movies)

    def get_top_rated_movies(self, limit: int) -> MovieResponseList:
        movies = [
            MovieResponse.model_validate(movie)
            for movie in self.movie_repository.get_top_rated_movies(limit)
        ]
        return MovieResponseList(movie_list=movies)

    def get_top_newest_movies(self, limit: int) -> MovieResponseList:
        movies = [
            MovieResponse.model_validate(movie)
            for movie in self.movie_repository.get_top_newest_movies(limit)
        ]
        return MovieResponseList(movie_list=movies)

    def get_top_oldest_movies(self, limit: int) -> MovieResponseList:
        movies = [
            MovieResponse.model_validate(movie)
            for movie in self.movie_repository.get_top_oldest_movies(limit)
        ]
        return MovieResponseList(movie_list=movies)

    def create_movie(self, create_movie_data: MovieCreate) -> MovieResponse:
        if self.movie_repository.movie_name_exists(create_movie_data.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Movie with movie_name={create_movie_data.name} already exists",
            )
        movie = self.movie_repository.create_movie(create_movie_data)
        return MovieResponse.model_validate(movie)

    def update_movie(
        self,
        movie_id: int,
        update_movie_data: MovieUpdate,
    ) -> MovieResponse:
        movie = self.movie_repository.get_movie_by_id(movie_id)
        if movie is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with {movie_id=} not found",
            )

        if (
            movie.name != update_movie_data.name
            and self.movie_repository.movie_name_exists(update_movie_data.name)
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Movie with movie_name={update_movie_data.name} already exists",
            )
        updated_movie = self.movie_repository.update_movie(movie_id, update_movie_data)
        return MovieResponse.model_validate(updated_movie)

    def partial_update_movie(
        self,
        movie_id: int,
        update_movie_data: MoviePartialUpdate,
    ) -> MovieResponse:
        movie = self.movie_repository.get_movie_by_id(movie_id)
        if movie is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with {movie_id=} not found",
            )

        if (
            "name" in update_movie_data.model_fields_set
            and movie.name != update_movie_data.name
            and self.movie_repository.movie_name_exists(update_movie_data.name)
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Movie with movie_name={update_movie_data.name} already exists",
            )
        updated_movie = self.movie_repository.partial_update_movie(
            movie_id, update_movie_data
        )
        return MovieResponse.model_validate(updated_movie)

    def delete_movie_by_id(self, movie_id: int) -> None:
        if not self.movie_repository.delete_movie_by_id(movie_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with {movie_id} not found",
            )
