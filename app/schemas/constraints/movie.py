from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import Field

from core.constants import (
    MOVIE_DESCRIPTION_MAX_LENGTH,
    MOVIE_NAME_MAX_LENGTH,
    MOVIE_NAME_MIN_LENGTH,
    MOVIE_RATING_MAX_VALUE,
    MOVIE_RATING_MIN_VALUE,
)

NameConstraint = Annotated[
    str,
    Len(
        min_length=MOVIE_NAME_MIN_LENGTH,
        max_length=MOVIE_NAME_MAX_LENGTH,
    ),
]
DescriptionConstraint = Annotated[
    str,
    MaxLen(max_length=MOVIE_DESCRIPTION_MAX_LENGTH),
]
RatingConstraint = Annotated[
    float,
    Field(
        ge=MOVIE_RATING_MIN_VALUE,
        le=MOVIE_RATING_MAX_VALUE,
    ),
]
