__all__ = ("router",)
from fastapi import APIRouter
from .list_views import router as list_users_router
from .details_views import router as details_users_router
from .details_views_login import router as details_users_router_login

router = APIRouter(
    tags=["Users"],
    prefix="/users",
)
router_by_login = APIRouter(prefix="/by-login")
router_by_login.include_router(details_users_router_login)
router.include_router(list_users_router)
router.include_router(details_users_router)
router.include_router(router_by_login)
