from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from packages.rabbit_mq.connection import close_rabbit_mq, init_rabbit_mq

from core.database.init_db import init_admin


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    """
    Действия до старта приложения.
    """
    await init_rabbit_mq()
    await init_admin()
    yield
    """
    Действия после заверения работы приложения.
    """
    await close_rabbit_mq()
