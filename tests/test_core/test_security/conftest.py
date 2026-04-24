import pytest

from core.constants import TOKEN_TYPE
from tests.utils import generate_random_string


@pytest.fixture(scope="function")
def payload() -> dict[str, str | int]:
    sub = generate_random_string()
    login = generate_random_string()
    email = generate_random_string()
    token_type = generate_random_string()
    data = {
        "sub": sub,
        "login": login,
        "email": email,
        TOKEN_TYPE: token_type,
    }

    return data
