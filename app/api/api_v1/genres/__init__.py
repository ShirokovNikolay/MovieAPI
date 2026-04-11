__all__ = ("router",)
from fastapi import APIRouter
from .list_views import router as list_genres_router
from .details_views import router as details_genres_router

router = APIRouter(
    tags=["Genres"],
    prefix="/genres",
)
router.include_router(list_genres_router)
router.include_router(details_genres_router)
