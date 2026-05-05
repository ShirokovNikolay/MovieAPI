from os import getenv
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession


from core.database.connection import session_factory


@pytest.fixture(scope="session", autouse=True)
def test_environment_is_ready() -> None:
    if getenv("TESTING") != "1":
        pytest.exit(
            reason="Environment is not ready!",
        )


@pytest.fixture(scope="function")
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as database_session:
        yield database_session
        await database_session.rollback()
