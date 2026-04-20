from fastapi import FastAPI

from api import router as api_router
from api.exception_handlers import register_exception_handlers
from api.main_views import router as main_router
from core.config import settings
from lifespan import lifespan

app = FastAPI(
    title="Movie API",
    debug=settings.debug,
    lifespan=lifespan,
)
register_exception_handlers(app)
app.include_router(main_router)
app.include_router(api_router)
