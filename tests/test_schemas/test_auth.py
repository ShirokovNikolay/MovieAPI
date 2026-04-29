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

    @pytest.mark.parametrize(
        "field,expected_error_message",
        [
            ("login", "Field required"),
            ("password", "Field required"),
        ],
    )
    def test_user_login_without_field(
        self,
        user_login_data: dict[str, str],
        field: str,
        expected_error_message: str,
    ) -> None:
        user_login_data.pop(field)
        with pytest.raises(ValidationError, match=expected_error_message):
            UserLogin(**user_login_data)

    @pytest.mark.parametrize(
        "field,value,expected_error_message",
        [
            (
                "login",
                generate_string(length=USER_LOGIN_MIN_LENGTH - 1),
                "string_too_short",
            ),
            (
                "password",
                generate_string(length=USER_PASSWORD_MIN_LENGTH - 1),
                "string_too_short",
            ),
            (
                "login",
                generate_string(length=USER_LOGIN_MAX_LENGTH + 1),
                "string_too_long",
            ),
            (
                "password",
                generate_string(length=USER_PASSWORD_MAX_LENGTH + 1),
                "string_too_long",
            ),
        ],
    )
    def test_user_login_with_not_valid_field_length(
        self,
        user_login_data: dict[str, str],
        field: str,
        value: str,
        expected_error_message: str,
    ) -> None:
        user_login_data[field] = value
        with pytest.raises(ValidationError, match=expected_error_message):
            UserLogin(**user_login_data)
