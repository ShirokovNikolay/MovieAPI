import pytest
from _pytest.fixtures import SubRequest

from core.constants import BASE_USER_ERROR
from core.exceptions.user import (
    UserNotFoundError,
    UserAlreadyExistsError,
    UserLoginAlreadyExistsError,
    UserEmailAlreadyExistsError,
    UserLoginNotFoundError,
    UserIdNotFoundError,
)


@pytest.fixture(
    scope="function",
    params=[
        UserNotFoundError,
        UserAlreadyExistsError,
    ],
)
def base_user_error(request: SubRequest) -> BASE_USER_ERROR:
    return request.param


def test_base_user_error_can_raise_with_detail(
    base_user_error: BASE_USER_ERROR, detail: str
) -> None:
    with pytest.raises(
        base_user_error,
        match=detail,
    ) as exc_info:
        raise base_user_error(detail)
    assert exc_info.value.detail == detail


def test_user_id_not_found_error_can_raise_with_detail(user_id: int) -> None:
    with pytest.raises(
        UserIdNotFoundError,
        match=str(user_id),
    ) as exc_info:
        raise UserIdNotFoundError(user_id)
    assert exc_info.value.user_id == user_id


def test_user_login_not_found_error_can_raise_with_detail(name: str) -> None:
    with pytest.raises(UserLoginNotFoundError, match=name) as exc_info:
        raise UserLoginNotFoundError(name)
    assert exc_info.value.login == name


def test_user_login_already_exists_error(name: str) -> None:
    with pytest.raises(
        UserLoginAlreadyExistsError,
        match=name,
    ) as exc_info:
        raise UserLoginAlreadyExistsError(name)
    assert exc_info.value.login == name


def test_user_email_already_exists_error(name: str) -> None:
    with pytest.raises(
        UserEmailAlreadyExistsError,
        match=name,
    ) as exc_info:
        raise UserEmailAlreadyExistsError(name)
    assert exc_info.value.email == name
