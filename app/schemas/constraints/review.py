from typing import Annotated

from annotated_types import MaxLen
from pydantic import Field

from core.constants import (
    REVIEW_RATING_MAX_VALUE,
    REVIEW_RATING_MIN_VALUE,
    REVIEW_TEXT_MAX_LENGTH,
)

ReviewTextConstraint = Annotated[
    str,
    MaxLen(max_length=REVIEW_TEXT_MAX_LENGTH),
]
RatingConstraint = Annotated[
    int,
    Field(
        ge=REVIEW_RATING_MIN_VALUE,
        le=REVIEW_RATING_MAX_VALUE,
    ),
]
