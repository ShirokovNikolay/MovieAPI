from pydantic import BaseModel

from core.constants import BEARER_TOKEN_TYPE


class TokenInfo(BaseModel):
    """
    Модель для вывода информации о токенах.
    """

    access_token: str
    refresh_token: str | None = None
    token_type: str = BEARER_TOKEN_TYPE


class TemporaryTokenInfo(BaseModel):
    """
    Модель для вывода информации о токенах,
    предназначенных для временного доступа к
    отправке кодов подтверждения на почту.
    """

    temporary_token: str
    token_type: str = BEARER_TOKEN_TYPE
