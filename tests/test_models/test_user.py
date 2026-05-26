import pytest
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import (
    USER_SURNAME_MIN_LENGTH,
    USER_SURNAME_MAX_LENGTH,
    USER_NAME_MIN_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_LOGIN_MIN_LENGTH,
    USER_LOGIN_MAX_LENGTH,
    USER_ENCRYPTED_PASSWORD_MAX_LENGTH,
    USER_EMAIL_MIN_LENGTH,
    USER_EMAIL_MAX_LENGTH,
)
from models import User
from tests.utils.data_generators.base import generate_string


class TestUserModel:
    async def test_create_user(
        self,
        session: AsyncSession,
        user_data_encrypted_password: dict,
    ) -> None:
        user = User(**user_data_encrypted_password)
        session.add(user)
        await session.flush()
        await session.refresh(user)
        assert user.id is not None
        assert user_data_encrypted_password["surname"] == user.surname
        assert user_data_encrypted_password["name"] == user.name
        assert user_data_encrypted_password["login"] == user.login
        assert user_data_encrypted_password["email"] == user.email
        assert (
            user_data_encrypted_password["encrypted_password"]
            == user.encrypted_password
        )

    @pytest.mark.parametrize(
        "field,value,expected_error",
        [
            (
                "role",
                generate_string(
                    min_string_length=10,
                    max_string_length=20,
                ),
                DBAPIError,
            ),
            (
                "surname",
                generate_string(
                    length=USER_SURNAME_MIN_LENGTH - 1,
                ),
                DBAPIError,
            ),
            (
                "surname",
                generate_string(
                    length=USER_SURNAME_MAX_LENGTH + 1,
                ),
                DBAPIError,
            ),
            (
                "name",
                generate_string(
                    length=USER_NAME_MIN_LENGTH - 1,
                ),
                DBAPIError,
            ),
            (
                "name",
                generate_string(
                    length=USER_NAME_MAX_LENGTH + 1,
                ),
                DBAPIError,
            ),
            (
                "login",
                generate_string(
                    length=USER_LOGIN_MIN_LENGTH - 1,
                ),
                DBAPIError,
            ),
            (
                "login",
                generate_string(
                    length=USER_LOGIN_MAX_LENGTH + 1,
                ),
                DBAPIError,
            ),
            (
                "email",
                generate_string(
                    length=USER_EMAIL_MIN_LENGTH - 1,
                ),
                DBAPIError,
            ),
            (
                "email",
                generate_string(
                    length=USER_EMAIL_MAX_LENGTH + 1,
                ),
                DBAPIError,
            ),
            (
                "encrypted_password",
                generate_string(
                    length=USER_ENCRYPTED_PASSWORD_MAX_LENGTH + 1,
                ),
                DBAPIError,
            ),
        ],
    )
    async def test_field_constraints_with_wrong_data(
        self,
        session: AsyncSession,
        user_data_encrypted_password: dict,
        field: str,
        value: str,
        expected_error,
    ) -> None:
        user_data_encrypted_password[field] = value
        user = User(**user_data_encrypted_password)
        session.add(user)
        with pytest.raises(expected_error):
            await session.flush()

    async def test_user_login_unique_constraint(
        self,
        session: AsyncSession,
        user_data_encrypted_password: dict[str, str],
        user: User,
    ) -> None:
        user_data_encrypted_password["login"] = user.login
        user_candidate = User(**user_data_encrypted_password)
        session.add(user_candidate)
        with pytest.raises(IntegrityError):
            await session.flush()

    async def test_user_email_unique_constraint(
        self,
        session: AsyncSession,
        user_data_encrypted_password: dict[str, str],
        user: User,
    ) -> None:
        user_data_encrypted_password["email"] = user.email
        user_candidate = User(**user_data_encrypted_password)
        session.add(user_candidate)
        with pytest.raises(IntegrityError):
            await session.flush()
