import random
import string

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


def generate_random_string(
    min_string_length: int = 1,
    max_string_length: int = 10,
    string_length: int | None = None,
) -> str:
    if string_length is None:
        string_length = random.randint(min_string_length, max_string_length)

    return "".join(
        [
            random.choice(
                string.ascii_letters + string.digits,
            )
            for _ in range(string_length)
        ],
    )


def generate_list_of_random_strings(
    min_string_length: int = 1,
    max_string_length: int = 10,
    string_length: int | None = None,
    min_list_length: int = 1,
    max_list_length: int = 5,
    list_length: int | None = None,
) -> list[str]:
    if list_length is None:
        list_length = random.randint(min_list_length, max_list_length)

    return [
        generate_random_string(
            min_string_length,
            max_string_length,
            string_length,
        )
        for _ in range(list_length)
    ]


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
