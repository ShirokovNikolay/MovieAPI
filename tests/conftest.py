from os import getenv

import pytest


@pytest.fixture(scope="session", autouse=True)
def test_environment_is_ready() -> None:
    if getenv("TESTING") != "1":
        pytest.exit(
            reason="Environment is not ready!",
        )
