from datetime import datetime

import pytest
from pydantic import ValidationError

from schemas.user import (
    UserResponse,
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponseList,
    UserPartialUpdate,
)
from core.constants import (
    USER_SURNAME_MIN_LENGTH,
    USER_SURNAME_MAX_LENGTH,
    USER_NAME_MIN_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_LOGIN_MIN_LENGTH,
    USER_LOGIN_MAX_LENGTH,
    USER_EMAIL_MIN_LENGTH,
    USER_EMAIL_MAX_LENGTH,
    USER_PASSWORD_MIN_LENGTH,
    USER_PASSWORD_MAX_LENGTH,
)
from tests.utils.data_generators.base import (
    generate_number,
    generate_string,
    check_schema_not_none_fields_is_valid,
)
from tests.utils.data_generators.user import (
    generate_random_email_fixed_length,
    create_user_data,
    create_user_data_response,
    create_user_response_list,
)


@pytest.fixture(scope="function")
def user_data() -> dict[str, str]:
    return create_user_data()


@pytest.fixture(scope="function")
def user_data_response() -> dict[str, str | int]:
    return create_user_data_response()


@pytest.fixture(scope="function")
def user_response_list() -> list[UserResponse]:
    return create_user_response_list(list_length=3)


@pytest.mark.parametrize(
    "schema",
    [
        UserBase,
        UserCreate,
        UserUpdate,
        UserResponse,
    ],
)
class TestUserBaseCreateUpdateResponse:
    def test_user(
        self,
        schema,
        user_data_response: dict[str, str | int],
    ) -> None:
        user = schema(**user_data_response)
        for field in user.model_dump():
            assert getattr(user, field) == user_data_response[field]

    def test_user_without_surname_field(
        self,
        schema,
        user_data_response: dict[str, str | int],
    ) -> None:
        user_data_response.pop("surname")
        with pytest.raises(ValidationError, match="Field required"):
            schema(**user_data_response)

    def test_user_without_name_field(
        self,
        schema,
        user_data_response: dict[str, str | int],
    ) -> None:
        user_data_response.pop("name")
        with pytest.raises(ValidationError, match="Field required"):
            schema(**user_data_response)

    def test_user_without_login_field(
        self,
        schema,
        user_data_response: dict[str, str | int],
    ) -> None:
        user_data_response.pop("login")
        with pytest.raises(ValidationError, match="Field required"):
            schema(**user_data_response)

    def test_user_without_email_field(
        self,
        schema,
        user_data_response: dict[str, str | int],
    ) -> None:
        user_data_response.pop("email")
        with pytest.raises(ValidationError, match="Field required"):
            schema(**user_data_response)

    def test_user_with_too_short_surname(
        self,
        schema,
        user_data_response: dict[str, str | int],
    ) -> None:
        user_data_response["surname"] = generate_string(
            string_length=USER_SURNAME_MIN_LENGTH - 1
        )
        with pytest.raises(ValidationError, match="string_too_short"):
            schema(**user_data_response)

    def test_user_with_too_long_surname(
        self,
        schema,
        user_data_response: dict[str, str | int],
    ) -> None:
        user_data_response["surname"] = generate_string(
            string_length=USER_SURNAME_MAX_LENGTH + 1
        )
        with pytest.raises(ValidationError, match="string_too_long"):
            schema(**user_data_response)

    def test_user_with_too_short_name(
        self,
        schema,
        user_data_response: dict[str, str | int],
    ) -> None:
        user_data_response["name"] = generate_string(
            string_length=USER_NAME_MIN_LENGTH - 1
        )
        with pytest.raises(ValidationError, match="string_too_short"):
            schema(**user_data_response)

    def test_user_with_too_long_name(
        self,
        schema,
        user_data_response: dict[str, str | int],
    ) -> None:
        user_data_response["name"] = generate_string(
            string_length=USER_NAME_MAX_LENGTH + 1
        )
        with pytest.raises(ValidationError, match="string_too_long"):
            schema(**user_data_response)

    def test_user_with_too_short_login(
        self,
        schema,
        user_data_response: dict[str, str | int],
    ) -> None:
        user_data_response["login"] = generate_string(
            string_length=USER_LOGIN_MIN_LENGTH - 1
        )
        with pytest.raises(ValidationError, match="string_too_short"):
            schema(**user_data_response)

    def test_user_with_too_long_login(
        self,
        schema,
        user_data_response: dict[str, str | int],
    ) -> None:
        user_data_response["login"] = generate_string(
            string_length=USER_LOGIN_MAX_LENGTH + 1
        )
        with pytest.raises(ValidationError, match="string_too_long"):
            schema(**user_data_response)

    def test_user_with_too_short_email(
        self,
        schema,
        user_data_response: dict[str, str | int],
    ) -> None:
        user_data_response["email"] = generate_random_email_fixed_length(
            email_length=USER_EMAIL_MIN_LENGTH - 1
        )
        with pytest.raises(ValidationError, match="too_short"):
            schema(**user_data_response)

    def test_user_with_too_long_email(
        self,
        schema,
        user_data_response: dict[str, str | int],
    ) -> None:
        user_data_response["email"] = generate_random_email_fixed_length(
            email_length=USER_EMAIL_MAX_LENGTH + 1
        )
        with pytest.raises(ValidationError, match="too_long"):
            schema(**user_data_response)


@pytest.mark.parametrize(
    "schema",
    [
        UserCreate,
        UserUpdate,
    ],
)
class TestUserCreateUpdate:
    def test_user_without_password(
        self,
        schema,
        user_data_response: dict[str, str | int],
    ) -> None:
        user_data_response.pop("password")
        with pytest.raises(ValidationError, match="Field required"):
            schema(**user_data_response)

    def test_user_with_too_short_password(
        self,
        schema,
        user_data_response: dict[str, str],
    ) -> None:
        user_data_response["password"] = generate_string(
            string_length=USER_PASSWORD_MIN_LENGTH - 1
        )
        with pytest.raises(ValidationError, match="string_too_short"):
            schema(**user_data_response)

    def test_user_with_too_long_password(
        self,
        schema,
        user_data_response: dict[str, str],
    ) -> None:
        user_data_response["password"] = generate_string(
            string_length=USER_PASSWORD_MAX_LENGTH + 1
        )
        with pytest.raises(ValidationError, match="string_too_long"):
            schema(**user_data_response)


class TestUserPartialUpdate:
    def test_user(
        self,
        user_data_response: dict[str, str | int],
    ) -> None:
        user = UserPartialUpdate(**user_data_response)
        for field in user.model_dump():
            assert getattr(user, field) == user_data_response[field]

    def test_user_partial_update_without_any_field(
        self,
        user_data: dict[str, str | datetime],
    ) -> None:
        user_data_copy = user_data.copy()
        for field in user_data:
            value = user_data_copy.pop(field)
            user_update_schema = UserPartialUpdate(**user_data_copy)
            check_schema_not_none_fields_is_valid(
                user_update_schema,
                user_data,
            )
            assert getattr(user_update_schema, field) is None
            user_data_copy[field] = value

    def test_user_with_too_short_surname(
        self,
        user_data: dict[str, str | int],
    ) -> None:
        user_data["surname"] = generate_string(
            string_length=USER_SURNAME_MIN_LENGTH - 1
        )
        with pytest.raises(ValidationError, match="string_too_short"):
            UserPartialUpdate(**user_data)

    def test_user_with_too_long_surname(
        self,
        user_data: dict[str, str | int],
    ) -> None:
        user_data["surname"] = generate_string(
            string_length=USER_SURNAME_MAX_LENGTH + 1
        )
        with pytest.raises(ValidationError, match="string_too_long"):
            UserPartialUpdate(**user_data)

    def test_user_with_too_short_name(
        self,
        user_data: dict[str, str | int],
    ) -> None:
        user_data["name"] = generate_string(string_length=USER_NAME_MIN_LENGTH - 1)
        with pytest.raises(ValidationError, match="string_too_short"):
            UserPartialUpdate(**user_data)

    def test_user_with_too_long_name(
        self,
        user_data: dict[str, str | int],
    ) -> None:
        user_data["name"] = generate_string(string_length=USER_NAME_MAX_LENGTH + 1)
        with pytest.raises(ValidationError, match="string_too_long"):
            UserPartialUpdate(**user_data)

    def test_user_with_too_short_login(
        self,
        user_data: dict[str, str | int],
    ) -> None:
        user_data["login"] = generate_string(string_length=USER_LOGIN_MIN_LENGTH - 1)
        with pytest.raises(ValidationError, match="string_too_short"):
            UserPartialUpdate(**user_data)

    def test_user_with_too_long_login(
        self,
        user_data: dict[str, str | int],
    ) -> None:
        user_data["login"] = generate_string(string_length=USER_LOGIN_MAX_LENGTH + 1)
        with pytest.raises(ValidationError, match="string_too_long"):
            UserPartialUpdate(**user_data)

    def test_user_with_too_short_email(
        self,
        user_data: dict[str, str | int],
    ) -> None:
        user_data["email"] = generate_random_email_fixed_length(
            email_length=USER_EMAIL_MIN_LENGTH - 1
        )
        with pytest.raises(ValidationError, match="too_short"):
            UserPartialUpdate(**user_data)

    def test_user_with_too_long_email(
        self,
        user_data: dict[str, str | int],
    ) -> None:
        user_data["email"] = generate_random_email_fixed_length(
            email_length=USER_EMAIL_MAX_LENGTH + 1
        )
        with pytest.raises(ValidationError, match="too_long"):
            UserPartialUpdate(**user_data)


class TestUserResponse:
    def test_user_without_id(
        self,
        user_data_response: dict[str, str | int],
    ) -> None:
        user_data_response.pop("id")
        with pytest.raises(ValidationError, match="Field required"):
            UserResponse(**user_data_response)

    def test_user_without_registration_date(
        self,
        user_data_response: dict[str, str | int],
    ) -> None:
        user_data_response.pop("registration_date")
        with pytest.raises(ValidationError, match="Field required"):
            UserResponse(**user_data_response)


class TestUserResponseList:
    def test_user_response_list(
        self,
        user_response_list: list[UserResponse],
    ) -> None:
        page = generate_number()
        size = generate_number()
        schema = UserResponseList(
            user_list=user_response_list,
            page=page,
            size=size,
        )
        assert schema.user_list == user_response_list
        assert schema.page == page
        assert schema.size == size

    def test_user_response_list_with_empty_list(self) -> None:
        page = generate_number()
        size = generate_number()
        schema = UserResponseList(
            user_list=[],
            page=page,
            size=size,
        )
        assert len(schema.user_list) == 0
        assert schema.page == page
        assert schema.size == size
