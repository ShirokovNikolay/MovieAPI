from .favorite_movie import FavoriteMovieRepository
from .genre import GenreRepository
from .movie import MovieRepository
from .review import ReviewRepository
from .user import UserRepository
from .watch_history import WatchHistoryRepository

__all__ = (
    "FavoriteMovieRepository",
    "GenreRepository",
    "MovieRepository",
    "ReviewRepository",
    "UserRepository",
    "WatchHistoryRepository",
)
