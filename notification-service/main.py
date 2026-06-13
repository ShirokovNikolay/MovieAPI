from fastapi import FastAPI

from api.main_views import router as main_router
from lifespan import lifespan

app = FastAPI(
    title="Notification Service",
    lifsepan=lifespan,
)

app.include_router(main_router)
