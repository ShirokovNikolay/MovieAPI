import pytest

from core.constants import TOKEN_TYPE
from core.security.validators import validate_token_payload
from tests.utils.data_generators.base import generate_string


def test_validate_token_payload_no_sub(payload: dict[str, str | int]) -> None:
    payload.pop("sub")
    with pytest.raises(KeyError):
        validate_token_payload(payload, target_token_type=payload[TOKEN_TYPE])


def test_validate_token_payload_invalid_data_token_type(
    payload: dict[str, str | int],
) -> None:
    with pytest.raises(TypeError):
        validate_token_payload(
            payload,
            target_token_type=payload[TOKEN_TYPE] + generate_string(),
        )
