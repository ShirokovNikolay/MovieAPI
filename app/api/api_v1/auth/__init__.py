__all__ = ("router",)

from fastapi import APIRouter

from .login_views import router as login_router
from .recover_views import router as recover_account_router
from .refresh_token_views import router as refresh_token_router
from .registration_views import router as registration_router

router = APIRouter(
    prefix="/auth",
)

router.include_router(registration_router)
router.include_router(login_router)
router.include_router(recover_account_router)
router.include_router(refresh_token_router)
