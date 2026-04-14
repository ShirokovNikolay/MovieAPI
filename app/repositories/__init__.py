from .genre import GenreRepository
from .movie import MovieRepository
from .review import ReviewRepository
from .user import UserRepository
from .favorite_movie import FavoriteMovieRepository
from .watch_history import WatchHistoryRepository

__all__ = (
    "GenreRepository",
    "MovieRepository",
    "ReviewRepository",
    "UserRepository",
    "FavoriteMovieRepository",
    "WatchHistoryRepository",
)
