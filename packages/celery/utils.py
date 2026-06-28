import asyncio
from collections.abc import Coroutine
from typing import Any


def sync_run_coroutine_function(coroutine: Coroutine) -> Any:
    return asyncio.run(coroutine)
