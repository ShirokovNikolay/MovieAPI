from core.constants import TOKEN_TYPE_FIELD


def validate_token_payload(
    payload: dict[str, str | int],
    target_token_type: str,
) -> None:
    if payload[TOKEN_TYPE_FIELD] != target_token_type:
        type_error_detail: str = "Invalid token type in payload"
        raise TypeError(type_error_detail)

    if "sub" not in payload:
        key_error_detail: str = "Missing parameter 'sub' in token payload"
        raise KeyError(key_error_detail)
