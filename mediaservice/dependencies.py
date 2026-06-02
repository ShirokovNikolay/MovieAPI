from collections.abc import AsyncGenerator
from typing import Annotated

from aioboto3 import Session
from fastapi import Depends
from types_aiobotocore_s3 import S3Client

from config import settings
from service import MinioService

S3_SESSION = Session()


def get_session() -> Session:
    global S3_SESSION  # noqa: PLW0602
    return S3_SESSION


async def get_client(
    session: Annotated[
        Session,
        Depends(get_session),
    ],
) -> AsyncGenerator[S3Client]:
    async with session.client(
        "s3",
        endpoint_url=settings.minio.endpoint_url,
        aws_access_key_id=settings.minio.access_key,
        aws_secret_access_key=settings.minio.secret_key,
    ) as client:
        yield client


async def get_minio_service(
    client: Annotated[
        S3Client,
        Depends(get_client),
    ],
) -> AsyncGenerator[MinioService]:
    minio_service = MinioService(
        client=client,
    )
    yield minio_service


MinioServiceDep = Annotated[
    MinioService,
    Depends(get_minio_service),
]
