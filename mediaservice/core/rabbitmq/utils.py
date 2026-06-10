from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from urllib.parse import urlsplit

from types_aiobotocore_s3 import S3Client

from core.config import settings
from dependencies import get_session
from minio_client import MinioClient
from service import MinioService


@asynccontextmanager
async def get_s3_client(
    service_name: str = "s3",
    endpoint_url: str = settings.minio.url_minio,
    aws_access_key_id: str = settings.minio.access_key,
    aws_secret_access_key: str = settings.minio.secret_key,
) -> AsyncGenerator[S3Client]:
    s3_session = get_session()
    async with s3_session.client(
        service_name=service_name,
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    ) as client:
        yield client


@asynccontextmanager
async def get_minio_client() -> AsyncGenerator[MinioClient]:
    async with get_s3_client() as client:
        minio_client = MinioClient(client=client)
        yield minio_client


@asynccontextmanager
async def get_minio_service() -> AsyncGenerator[MinioService]:
    async with get_minio_client() as minio_client:
        minio_service = MinioService(minio_client=minio_client)
        yield minio_service


def get_object_name_from_url(object_url: str, bucket_name: str) -> str:
    url_parts = urlsplit(object_url)
    path_url = url_parts.path
    bucket_name_part = "/" + bucket_name + "/"
    object_name = path_url.replace(bucket_name_part, "")
    return object_name
