from pydantic import BaseModel


class TokenInfo(BaseModel):
    """
    Модель для вывода информации о токенах.
    """

    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
