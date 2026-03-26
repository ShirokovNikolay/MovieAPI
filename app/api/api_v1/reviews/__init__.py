__all__ = ("router",)

from fastapi import APIRouter
from .list_views import router as list_reviews_router
from .details_movie_views import router as details_movie_router
from .details_user_views import router as details_user_router
from .details_review_views import router as details_review_router

router = APIRouter(
    tags=["Reviews"],
    prefix="/reviews",
)
movie_router = APIRouter(prefix="/movie")
user_router = APIRouter(prefix="/user")
movie_router.include_router(details_movie_router)
user_router.include_router(details_user_router)


router.include_router(list_reviews_router)
router.include_router(movie_router)
router.include_router(user_router)
router.include_router(details_review_router)
