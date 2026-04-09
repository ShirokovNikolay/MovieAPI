__all__ = ("router",)
from fastapi import APIRouter
from .genres import router as genres_router
from .movies import router as movies_router
from .reviews import router as reviews_router
from .users import router as users_router
from .auth import router as auth_router
from .favorite_movies import router as favorite_movies_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(auth_router)
router.include_router(genres_router)
router.include_router(movies_router)
router.include_router(users_router)
router.include_router(reviews_router)
router.include_router(favorite_movies_router)
