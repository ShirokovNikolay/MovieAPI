from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from packages.rabbitmq.connection import close_rabbitmq

from core.database.init_db import init_admin
from core.rabbitmq.prestart import start_rabbitmq


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    """
    Действия до старта приложения.
    """
    await init_admin()
    rabbitmq = start_rabbitmq()
    await anext(rabbitmq)
    yield
    """
    Действия после заверения работы приложения.
    """
    await rabbitmq.aclose()
    await close_rabbitmq()
