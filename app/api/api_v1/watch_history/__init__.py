__all__ = ("router",)

from fastapi import APIRouter, Depends

from dependencies.rate_limiter import check_rate_limit_auth

from .details_views import router as details_router
from .list_views import router as list_router

router = APIRouter(
    prefix="/watch-history",
    tags=["Watch History"],
    dependencies=[
        Depends(check_rate_limit_auth),
    ],
)
router.include_router(list_router)
router.include_router(details_router)
