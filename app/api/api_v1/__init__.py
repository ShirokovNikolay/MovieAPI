__all__ = ("router",)
from fastapi import APIRouter

from api.api_v1.auth import router as auth_router

from .favorite_movies import router as favorite_movies_router
from .genres import router as genres_router
from .media import router as media_router
from .movies import router as movies_router
from .reviews import router as reviews_router
from .users import router as users_router
from .watch_history import router as watch_history_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(auth_router)
router.include_router(media_router)
router.include_router(genres_router)
router.include_router(movies_router)
router.include_router(reviews_router)
router.include_router(favorite_movies_router)
router.include_router(watch_history_router)
router.include_router(users_router)
