from fastapi import FastAPI

from api import router as api_router
from api.main_views import router as main_router
from lifespan import lifespan

app = FastAPI(
    title="Media Service",
    lifespan=lifespan,
)
app.include_router(main_router)
app.include_router(api_router)
