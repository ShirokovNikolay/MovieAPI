__all__ = ("router",)

from fastapi import APIRouter

from .details_user_views import router as details_user_router
from .list_views import router as list_views_router

router = APIRouter(
    prefix="/favorite-movies",
    tags=["Favorite Movies"],
)
list_views_router.include_router(details_user_router)
router.include_router(list_views_router)
