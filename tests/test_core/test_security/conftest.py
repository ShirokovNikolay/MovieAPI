import pytest

from core.constants import TOKEN_TYPE
from tests.utils.data_generators.base import generate_string


@pytest.fixture(scope="function")
def payload() -> dict[str, str | int]:
    sub = generate_string()
    login = generate_string()
    email = generate_string()
    token_type = generate_string()
    data = {
        "sub": sub,
        "login": login,
        "email": email,
        TOKEN_TYPE: token_type,
    }

    return data
