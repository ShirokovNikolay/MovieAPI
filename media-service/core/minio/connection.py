from aioboto3 import Session

S3_SESSION = Session()


def get_session() -> Session:
    """
    Метод для получения сессии s3 хранилища.
    """
    global S3_SESSION  # noqa: PLW0602
    return S3_SESSION
