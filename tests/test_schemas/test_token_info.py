import pytest
from pydantic import ValidationError

from core.constants import BEARER_TOKEN_TYPE
from schemas.token_info import TokenInfo
from tests.utils import generate_random_string


def create_token_info_data():
    data = {
        "access_token": generate_random_string(),
        "refresh_token": generate_random_string(),
        "token_type": generate_random_string(),
    }
    return data


@pytest.fixture(scope="function")
def token_info_data():
    return create_token_info_data()


class TestTokenInfo:
    def test_token_info_schema(self, token_info_data: dict[str, str]) -> None:
        token_info_schema = TokenInfo(**token_info_data)
        assert token_info_schema.model_dump() == token_info_data

    def test_token_info_without_access_token(
        self, token_info_data: dict[str, str]
    ) -> None:
        token_info_data.pop("access_token")
        with pytest.raises(ValidationError, match="Field required"):
            TokenInfo(**token_info_data)

    def test_token_info_without_refresh_token(
        self, token_info_data: dict[str, str]
    ) -> None:
        token_info_data.pop("refresh_token")
        token_info = TokenInfo(**token_info_data)
        assert token_info.access_token == token_info_data["access_token"]
        assert token_info.refresh_token is None
        assert token_info.token_type == token_info_data["token_type"]

    def test_token_info_without_token_type(
        self, token_info_data: dict[str, str]
    ) -> None:
        token_info_data.pop("token_type")
        token_info = TokenInfo(**token_info_data)
        assert token_info.access_token == token_info_data["access_token"]
        assert token_info.refresh_token == token_info_data["refresh_token"]
        assert token_info.token_type == BEARER_TOKEN_TYPE
