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
    generate_email_fixed_length,
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
        UserPartialUpdate,
        UserResponse,
    ],
)
class TestUserBaseCreateUpdatePartialUpdateResponse:
    def test_user(
        self,
        schema,
        user_data_response: dict[str, str | int],
    ) -> None:
        user = schema(**user_data_response)
        for field in user.model_dump():
            assert getattr(user, field) == user_data_response[field]

    @pytest.mark.parametrize(
        "field,value,expected_error_message",
        [
            (
                "surname",
                generate_string(length=USER_SURNAME_MIN_LENGTH - 1),
                "string_too_short",
            ),
            (
                "name",
                generate_string(length=USER_NAME_MIN_LENGTH - 1),
                "string_too_short",
            ),
            (
                "login",
                generate_string(length=USER_LOGIN_MIN_LENGTH - 1),
                "string_too_short",
            ),
            (
                "email",
                generate_email_fixed_length(length=USER_EMAIL_MIN_LENGTH - 1),
                "too_short",
            ),
            (
                "surname",
                generate_string(length=USER_SURNAME_MAX_LENGTH + 1),
                "string_too_long",
            ),
            (
                "name",
                generate_string(length=USER_NAME_MAX_LENGTH + 1),
                "string_too_long",
            ),
            (
                "login",
                generate_string(length=USER_LOGIN_MAX_LENGTH + 1),
                "string_too_long",
            ),
            (
                "email",
                generate_email_fixed_length(length=USER_EMAIL_MAX_LENGTH + 1),
                "too_long",
            ),
        ],
    )
    def test_user_with_not_valid_field_length(
        self,
        schema,
        field: str,
        value: str,
        expected_error_message: str,
        user_data_response: dict[str, str | int],
    ) -> None:
        user_data_response[field] = value
        with pytest.raises(ValidationError, match=expected_error_message):
            schema(**user_data_response)

    @pytest.mark.parametrize(
        "field",
        [
            "surname",
            "name",
            "login",
            "email",
        ],
    )
    def test_user_without_field(
        self,
        schema,
        field: str,
        user_data_response: dict[str, str | int],
    ) -> None:
        if schema is UserPartialUpdate:
            pytest.skip(
                reason="UserPartialUpdate schema does does not have required fields"
            )
        user_data_response.pop(field)
        with pytest.raises(ValidationError, match="Field required"):
            schema(**user_data_response)


@pytest.mark.parametrize(
    "schema",
    [
        UserCreate,
        UserUpdate,
    ],
)
class TestUserCreateUpdate:
    def test_user_without_password_field(
        self,
        schema,
        user_data_response: dict[str, str | int],
    ) -> None:
        user_data_response.pop("password")
        with pytest.raises(ValidationError, match="Field required"):
            schema(**user_data_response)

    @pytest.mark.parametrize(
        "field,value,expected_error_message",
        [
            (
                "password",
                generate_string(length=USER_PASSWORD_MIN_LENGTH - 1),
                "string_too_short",
            ),
            (
                "password",
                generate_string(length=USER_PASSWORD_MAX_LENGTH + 1),
                "string_too_long",
            ),
        ],
    )
    def test_user_with_not_valid_field_length(
        self,
        schema,
        field: str,
        value: str,
        expected_error_message: str,
        user_data_response: dict[str, str | int],
    ) -> None:
        user_data_response[field] = value
        with pytest.raises(ValidationError, match=expected_error_message):
            schema(**user_data_response)


class TestUserPartialUpdate:
    def test_user(
        self,
        user_data_response: dict[str, str | int],
    ) -> None:
        user = UserPartialUpdate(**user_data_response)
        for field in user.model_dump():
            assert getattr(user, field) == user_data_response[field]

    def test_user_partial_update_without_field(
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


class TestUserResponse:
    @pytest.mark.parametrize(
        "field",
        [
            "id",
            "registration_date",
        ],
    )
    def test_user_without_field(
        self, user_data_response: dict[str, str | int], field: str
    ) -> None:
        user_data_response.pop(field)
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
