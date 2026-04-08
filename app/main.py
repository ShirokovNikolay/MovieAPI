from fastapi import FastAPI

from core.config import settings
from api import router as api_router
from api.main_views import router as main_router
from lifespan import lifespan
from api.exception_handlers import register_exception_handlers


app = FastAPI(
    title="Movie API",
    debug=settings.debug,
    lifespan=lifespan,
)
register_exception_handlers(app)
app.include_router(main_router)
app.include_router(api_router)
