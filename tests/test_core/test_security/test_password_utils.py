import pytest
from _pytest.fixtures import SubRequest

from core.security.password_utils import hash_password, verify_password
from tests.test_core.test_exceptions.test_base import (
    generate_list_of_random_strings,
    generate_random_string,
)


@pytest.fixture(
    scope="function",
    params=generate_list_of_random_strings(list_length=3),
)
def password(request: SubRequest) -> str:
    return request.param


def test_encrypt_and_decrypt_password(password: str) -> None:
    encoded_password = hash_password(password)
    assert verify_password(password, encoded_password)


@pytest.mark.xfail
def test_password_encryption_is_reproducible(password: str) -> None:
    encoded_password1 = hash_password(password)
    encoded_password2 = hash_password(password)
    assert encoded_password1 == encoded_password2


@pytest.mark.xfail
def test_verify_wrong_password(password: str) -> None:
    wrong_password = password + generate_random_string()
    encoded_wrong_password = hash_password(wrong_password)
    assert verify_password(password, encoded_wrong_password)
