import pytest

from core.constants import TOKEN_TYPE
from core.security.validators import validate_token_payload
from tests.test_core.test_exceptions.conftest import generate_random_string
from tests.test_core.test_security.conftest import payload


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
            target_token_type=payload[TOKEN_TYPE] + generate_random_string(),
        )
