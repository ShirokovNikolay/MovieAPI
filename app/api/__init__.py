__all__ = ["router"]
from fastapi import APIRouter
from .main_views import router as main_router

router = APIRouter()
router.include_router(main_router)
