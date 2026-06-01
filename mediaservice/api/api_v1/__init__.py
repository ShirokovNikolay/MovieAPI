from fastapi import APIRouter

from .file_views import router as file_view_router

router = APIRouter(
    prefix="/v1",
)
router.include_router(file_view_router)
