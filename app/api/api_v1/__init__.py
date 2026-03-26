__all__ = ("router",)
from fastapi import APIRouter
from .genres import router as genres_router
from .movies import router as movies_router

router = APIRouter(
    prefix="/v1",
)
router.include_router(genres_router)
router.include_router(movies_router)
