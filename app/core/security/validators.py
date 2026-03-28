from fastapi import HTTPException
from starlette import status

from core.constants import TOKEN_TYPE


def validate_token_payload(
    payload: dict,
    target_token_type: str,
) -> None:
    if payload[TOKEN_TYPE] != target_token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    if "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token content",
        )
