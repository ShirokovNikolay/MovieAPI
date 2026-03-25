from fastapi import FastAPI
from config import settings
from api import router as api_router
from api.main_views import router as main_router
from lifespan import lifespan

app = FastAPI(
    title="Movie API",
    debug=settings.debug,
    lifespan=lifespan,
)
app.include_router(main_router)
app.include_router(api_router)
