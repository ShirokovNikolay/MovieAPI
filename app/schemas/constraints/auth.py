from typing import Annotated

from annotated_types import Len

from core.constants import CONFIRMATION_CODE_LENGTH

ConfirmationCodeConstraint = Annotated[
    str,
    Len(
        min_length=CONFIRMATION_CODE_LENGTH,
        max_length=CONFIRMATION_CODE_LENGTH,
    ),
]
