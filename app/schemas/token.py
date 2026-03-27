from pydantic import BaseModel


class TokenInfo(BaseModel):
    """
    Модель для вывода информации о токене.
    """

    access_token: str
    token_type: str
