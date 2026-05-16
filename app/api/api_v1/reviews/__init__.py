__all__ = ("router",)

from fastapi import APIRouter

from .details_movie_views import router as details_movie_router
from .details_review_views import router as details_review_router
from .details_user_views import router as details_user_router
from .list_views import router as list_reviews_router

router = APIRouter(
    tags=["Reviews"],
    prefix="/reviews",
)
movie_router = APIRouter(prefix="/movie")

movie_router.include_router(details_movie_router)
router.include_router(list_reviews_router)
router.include_router(movie_router)
router.include_router(details_user_router)
router.include_router(details_review_router)
