from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from packages.rabbitmq.connection import rabbitmq_connection_shutdown

from core.rabbitmq.startup import rabbitmq_startup


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    """
    Действия до старта приложения.
    """
    rabbitmq = rabbitmq_startup()
    await anext(rabbitmq)
    yield
    """
    Действия после заверения работы приложения.
    """
    await rabbitmq.aclose()
    await rabbitmq_connection_shutdown()
