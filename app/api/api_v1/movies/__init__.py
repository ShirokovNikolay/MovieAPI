__all__ = ("router",)

from fastapi import APIRouter
from .list_views import router as list_movies_router
from .details_views import router as details_movies_router
from .details_views_name import router as details_movies_router_name

router = APIRouter(
    tags=["Movies"],
    prefix="/movies",
)
name_router = APIRouter(
    prefix="/by-name",
)
name_router.include_router(details_movies_router_name)


router.include_router(list_movies_router)
router.include_router(details_movies_router)
router.include_router(name_router)
