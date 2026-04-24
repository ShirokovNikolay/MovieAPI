import pytest
from _pytest.fixtures import SubRequest

from core.constants import BASE_ERROR
from core.exceptions.base import (
    AuthenticationError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    TooManyRequestsError,
)


@pytest.fixture(
    scope="function",
    params=[
        NotFoundError,
        ConflictError,
        ForbiddenError,
        AuthenticationError,
        TooManyRequestsError,
    ],
)
def base_error(
    request: SubRequest,
) -> BASE_ERROR:
    return request.param


def test_base_error_can_raise_with_detail(
    detail: str,
    base_error: BASE_ERROR,
) -> None:
    with pytest.raises(
        base_error,
        match=detail,
    ) as exc_info:
        raise base_error(detail)
    assert exc_info.value.detail == detail


def test_error_inherits_from_base_exception(base_error) -> None:
    assert issubclass(base_error, Exception)
