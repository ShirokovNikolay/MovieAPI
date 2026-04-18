from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.database.init_db import init_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Действия до старта приложения.
    """
    await init_admin()
    yield
    """
    Действия после заверения работы приложения.
    """
