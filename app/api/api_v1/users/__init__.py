__all__ = ("router",)
from fastapi import APIRouter, Depends

from dependencies.rate_limiter import check_rate_limit_auth
from .list_views import router as list_users_router
from .details_views import router as details_users_router
from .details_views_login import router as details_users_router_login
from .profile_views import router as profile_users_router

router = APIRouter(
    tags=["Users"],
    prefix="/users",
    dependencies=[
        Depends(check_rate_limit_auth),
    ],
)
router.include_router(profile_users_router)
router_by_login = APIRouter(prefix="/by-login")
router_by_login.include_router(details_users_router_login)
router.include_router(list_users_router)
router.include_router(details_users_router)
router.include_router(router_by_login)
