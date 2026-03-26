__all__ = ("router",)
from fastapi import APIRouter
from .genres import router as genres_router
from .movies import router as movies_router
from .reviews import router as reviews_router
from .users import router as users_router

router = APIRouter(
    prefix="/v1",
)
router.include_router(genres_router)
router.include_router(movies_router)
router.include_router(users_router)
router.include_router(reviews_router)
