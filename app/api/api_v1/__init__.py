__all__ = ("router",)
from fastapi import APIRouter
from .genres import router as genres_router

router = APIRouter(
    prefix="/v1",
)
router.include_router(genres_router)
