from os import getenv
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)


from core.config import settings


@pytest.fixture(scope="session", autouse=True)
def test_environment_is_ready() -> None:
    if getenv("TESTING") != "1":
        pytest.exit(
            reason="Environment is not ready!",
        )


@pytest.fixture(scope="function")
async def engine() -> AsyncEngine:
    return create_async_engine(
        url=settings.database.url_database,
    )


@pytest.fixture(scope="function")
async def session_factory(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(bind=engine)


@pytest.fixture(scope="function")
async def session(
    session_factory: async_sessionmaker,
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as database_session:
        yield database_session
        await database_session.rollback()
