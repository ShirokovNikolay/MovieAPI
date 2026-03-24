from sqlalchemy.orm import Session

from repositories import GenreRepository, MovieRepository
from fastapi import HTTPException, status

from schemas.genre import (
    GenreCreate,
    GenreUpdate,
    GenreResponse,
    GenrePartialUpdate,
    GenreResponseList,
)


class GenreService:
    def __init__(self, session: Session) -> None:
        self.genre_repository = GenreRepository(session)
        self.movie_repository = MovieRepository(session)

    def get_genre_by_id(self, genre_id: int) -> GenreResponse:
        genre = self.genre_repository.get_genre_by_id(genre_id)
        if genre is not None:
            return GenreResponse.model_validate(genre)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genre with {genre_id=} does not exist",
        )

    def get_genre_by_name(self, genre_name: str) -> GenreResponse:
        genre = self.genre_repository.get_genre_by_name(genre_name)
        if genre is not None:
            return GenreResponse.model_validate(genre)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genre with {genre_name=} does not exist",
        )

    def get_all_genres(self) -> GenreResponseList:
        genres = [
            GenreResponse.model_validate(genre)
            for genre in self.genre_repository.get_all_genres()
        ]
        return GenreResponseList(genre_list=genres)

    def create_genre(self, create_data: GenreCreate) -> GenreResponse:
        genre = self.genre_repository.create_genre(create_data)
        return GenreResponse.model_validate(genre)

    def update_genre(self, genre_id: int, update_data: GenreUpdate) -> GenreResponse:
        genre = self.genre_repository.update_genre(genre_id, update_data)
        if genre is not None:
            return GenreResponse.model_validate(genre)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genre with {genre_id=} not found",
        )

    def partial_update_genre(
        self, genre_id: int, update_data: GenrePartialUpdate
    ) -> GenreResponse:
        genre = self.genre_repository.partial_update_genre(genre_id, update_data)
        if genre is not None:
            return GenreResponse.model_validate(genre)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genre with {genre_id=} not found",
        )

    def delete_genre_by_id(self, genre_id: int) -> None:
        movies = self.movie_repository.get_movies_by_genre_id(genre_id)
        if movies:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Movies with {genre_id=} already exist",
            )

        if not self.genre_repository.delete_genre_by_id(genre_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Genre with {genre_id=} does not exist",
            )

    def delete_genre_by_name(self, genre_name: str) -> None:
        movies = self.movie_repository.get_movies_by_genre_name(genre_name)
        if movies:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Movies with {genre_name=} already exist",
            )

        if not self.genre_repository.delete_genre_by_name(genre_name):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Genre with {genre_name=} does not exist",
            )
