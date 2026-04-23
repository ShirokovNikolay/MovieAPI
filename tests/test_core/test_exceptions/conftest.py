import pytest
from _pytest.fixtures import SubRequest

from tests.test_core.test_exceptions.test_base import generate_list_of_random_strings


@pytest.fixture(
    scope="function",
    params=generate_list_of_random_strings(
        list_length=3,
    ),
)
def detail(request: SubRequest) -> str:
    return request.param
