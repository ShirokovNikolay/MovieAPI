from typing import Annotated

from annotated_types import Len, MaxLen

from core.constants import (
    GENRE_DESCRIPTION_MAX_LENGTH,
    GENRE_NAME_MAX_LENGTH,
    GENRE_NAME_MIN_LENGTH,
)

NameConstraint = Annotated[
    str,
    Len(
        min_length=GENRE_NAME_MIN_LENGTH,
        max_length=GENRE_NAME_MAX_LENGTH,
    ),
]
DescriptionConstraint = Annotated[
    str,
    MaxLen(max_length=GENRE_DESCRIPTION_MAX_LENGTH),
]
