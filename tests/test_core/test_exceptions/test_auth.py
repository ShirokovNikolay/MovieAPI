import pytest
from _pytest.fixtures import SubRequest

from core.constants import BASE_AUTH_ERROR
from core.exceptions.auth import (
    PermissionDeniedError,
    InvalidPasswordError,
    InvalidTokenError,
)


@pytest.fixture(
    scope="function",
    params=[
        InvalidPasswordError,
        PermissionDeniedError,
    ],
)
def base_auth_error_with_no_detail(request: SubRequest) -> BASE_AUTH_ERROR:
    return request.param


@pytest.fixture(
    scope="function",
    params=[
        InvalidTokenError,
    ],
)
def base_auth_error_with_detail(request: SubRequest) -> BASE_AUTH_ERROR:
    return request.param


def test_base_auth_error_with_no_detail_can_raise(
    base_auth_error_with_no_detail: BASE_AUTH_ERROR,
) -> None:
    with pytest.raises(base_auth_error_with_no_detail):
        raise base_auth_error_with_no_detail


def test_base_auth_error_can_raise_with_detail(
    base_auth_error_with_detail: BASE_AUTH_ERROR,
    detail: str,
) -> None:
    with pytest.raises(
        base_auth_error_with_detail,
        match=detail,
    ) as exc_info:
        raise base_auth_error_with_detail(detail)
    assert exc_info.value.detail == detail
