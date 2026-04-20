from core.constants import TOKEN_TYPE


def validate_token_payload(
    payload: dict[str, str | int],
    target_token_type: str,
) -> None:
    if payload[TOKEN_TYPE] != target_token_type:
        raise TypeError("Invalid token type in payload")

    if "sub" not in payload:
        raise KeyError("Missing parameter 'sub' in token payload")
