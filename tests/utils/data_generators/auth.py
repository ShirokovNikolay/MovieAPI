from core.constants import (
    USER_LOGIN_MIN_LENGTH,
    USER_LOGIN_MAX_LENGTH,
    USER_PASSWORD_MIN_LENGTH,
    USER_PASSWORD_MAX_LENGTH,
)
from tests.utils.data_generators.base import generate_string


def create_user_login_data() -> dict[str, str]:
    data = {
        "login": generate_string(
            min_string_length=USER_LOGIN_MIN_LENGTH,
            max_string_length=USER_LOGIN_MAX_LENGTH,
        ),
        "password": generate_string(
            min_string_length=USER_PASSWORD_MIN_LENGTH,
            max_string_length=USER_PASSWORD_MAX_LENGTH,
        ),
    }
    return data
