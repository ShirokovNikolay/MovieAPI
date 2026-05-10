__all__ = ("router",)
from fastapi import APIRouter, Depends

from dependencies.rate_limiter import check_rate_limit_auth

from .details_views import router as details_users_router
from .profile_views import router as profile_users_router

router = APIRouter(
    tags=["Users"],
    prefix="/users",
    dependencies=[
        Depends(check_rate_limit_auth),
    ],
)
router.include_router(profile_users_router)
router.include_router(details_users_router)
