__all__ = ("router",)

from fastapi import APIRouter

from .send_email_views import router as send_email_views_router

router = APIRouter(prefix="/v1")
router.include_router(send_email_views_router)
