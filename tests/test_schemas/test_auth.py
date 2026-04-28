import pytest
from pydantic import ValidationError

from schemas.auth import UserLogin
from tests.test_schemas.test_user import (
    LOGIN_MIN_LENGTH,
    LOGIN_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    PASSWORD_MAX_LENGTH,
)
from tests.utils import generate_random_string


def create_user_login_data() -> dict[str, str]:
    data = {
        "login": generate_random_string(
            min_string_length=LOGIN_MIN_LENGTH,
            max_string_length=LOGIN_MAX_LENGTH,
        ),
        "password": generate_random_string(
            min_string_length=PASSWORD_MIN_LENGTH,
            max_string_length=PASSWORD_MAX_LENGTH,
        ),
    }
    return data


@pytest.fixture(scope="function")
def user_login_data():
    return create_user_login_data()


class TestUserLogin:
    def test_user_login(self, user_login_data: dict[str, str]) -> None:
        user_login = UserLogin(**user_login_data)
        assert user_login.model_dump() == user_login_data

    def test_user_login_without_login_field(
        self, user_login_data: dict[str, str]
    ) -> None:
        user_login_data.pop("login")
        with pytest.raises(ValidationError, match="Field required"):
            UserLogin(**user_login_data)

    def test_user_login_without_password_field(
        self, user_login_data: dict[str, str]
    ) -> None:
        user_login_data.pop("password")
        with pytest.raises(ValidationError, match="Field required"):
            UserLogin(**user_login_data)

    def test_user_with_too_short_login(
        self,
        user_login_data: dict[str, str],
    ) -> None:
        user_login_data["login"] = generate_random_string(
            string_length=LOGIN_MIN_LENGTH - 1
        )
        with pytest.raises(ValidationError, match="string_too_short"):
            UserLogin(**user_login_data)

    def test_user_with_too_long_login(
        self,
        user_login_data: dict[str, str],
    ) -> None:
        user_login_data["login"] = generate_random_string(
            string_length=LOGIN_MAX_LENGTH + 1
        )
        with pytest.raises(ValidationError, match="string_too_long"):
            UserLogin(**user_login_data)

    def test_user_with_too_short_password(
        self,
        user_login_data: dict[str, str],
    ) -> None:
        user_login_data["password"] = generate_random_string(
            string_length=PASSWORD_MIN_LENGTH - 1
        )
        with pytest.raises(ValidationError, match="string_too_short"):
            UserLogin(**user_login_data)

    def test_user_with_too_long_password(
        self,
        user_login_data: dict[str, str],
    ) -> None:
        user_login_data["password"] = generate_random_string(
            string_length=PASSWORD_MAX_LENGTH + 1
        )
        with pytest.raises(ValidationError, match="string_too_long"):
            UserLogin(**user_login_data)
