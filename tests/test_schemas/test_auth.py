import pytest
from pydantic import ValidationError

from schemas.auth import UserLogin
from core.constants import (
    USER_LOGIN_MIN_LENGTH,
    USER_LOGIN_MAX_LENGTH,
    USER_PASSWORD_MIN_LENGTH,
    USER_PASSWORD_MAX_LENGTH,
)
from tests.utils.data_generators.auth import create_user_login_data
from tests.utils.data_generators.base import generate_string


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
        user_login_data["login"] = generate_string(length=USER_LOGIN_MIN_LENGTH - 1)
        with pytest.raises(ValidationError, match="string_too_short"):
            UserLogin(**user_login_data)

    def test_user_with_too_long_login(
        self,
        user_login_data: dict[str, str],
    ) -> None:
        user_login_data["login"] = generate_string(length=USER_LOGIN_MAX_LENGTH + 1)
        with pytest.raises(ValidationError, match="string_too_long"):
            UserLogin(**user_login_data)

    def test_user_with_too_short_password(
        self,
        user_login_data: dict[str, str],
    ) -> None:
        user_login_data["password"] = generate_string(
            length=USER_PASSWORD_MIN_LENGTH - 1
        )
        with pytest.raises(ValidationError, match="string_too_short"):
            UserLogin(**user_login_data)

    def test_user_with_too_long_password(
        self,
        user_login_data: dict[str, str],
    ) -> None:
        user_login_data["password"] = generate_string(
            length=USER_PASSWORD_MAX_LENGTH + 1
        )
        with pytest.raises(ValidationError, match="string_too_long"):
            UserLogin(**user_login_data)
