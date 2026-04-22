from os import getenv

import pytest

if getenv("TESTING") != "1":
    pytest.exit(
        reason="Environment is not ready!",
    )
