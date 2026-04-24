from typing import Any

import pytest

from core.security.jwt_utils import encode_jwt, decode_jwt


@pytest.fixture(scope="function")
def jwt_token(payload: dict[str, Any]) -> str:
    return encode_jwt(payload)


def test_can_encode_and_decode_jwt(payload: dict[str, Any]) -> None:
    jwt_token = encode_jwt(payload)
    decode_payload = decode_jwt(jwt_token)
    for key, value in payload.items():
        assert key in decode_payload
        assert value == decode_payload[key]


def test_decoded_jwt_payload_has_iat_field(jwt_token: str) -> None:
    payload = decode_jwt(jwt_token)
    assert payload.get("iat", 0) > 0


def test_decoded_jwt_payload_has_exp_field(jwt_token: str) -> None:
    payload = decode_jwt(jwt_token)
    assert payload.get("exp", 0) > 0
