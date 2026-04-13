__all__ = ("router",)

from fastapi import APIRouter, Depends

from dependencies.redis import rate_limit_movie
from .list_views import router as list_movies_router
from .details_views import router as details_movies_router

router = APIRouter(
    tags=["Movies"],
    prefix="/movies",
    dependencies=[Depends(rate_limit_movie)],
)


router.include_router(list_movies_router)
router.include_router(details_movies_router)
