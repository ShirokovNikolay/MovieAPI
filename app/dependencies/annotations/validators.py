from typing import Annotated

from fastapi import Query

PaginationSizeDep = Annotated[
    int,
    Query(
        ge=1,
    ),
]

PaginationPageDep = Annotated[
    int,
    Query(
        ge=1,
    ),
]
