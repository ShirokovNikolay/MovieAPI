__all__ = ("router",)

from fastapi import APIRouter, Depends

from .list_views import router as list_movies_router
from .details_views import router as details_movies_router

router = APIRouter(
    tags=["Movies"],
    prefix="/movies",
)


router.include_router(list_movies_router)
router.include_router(details_movies_router)
