from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import cast

from aio_pika.abc import AbstractChannel
from packages.rabbit_mq import RabbitMQService, connection
from types_aiobotocore_s3 import S3Client

from config import settings
from dependencies import S3_SESSION
from minio_client import MinioClient


@asynccontextmanager
async def get_s3_client(
    service_name: str = "s3",
    endpoint_url: str = settings.minio.url_minio,
    aws_access_key_id: str = settings.minio.access_key,
    aws_secret_access_key: str = settings.minio.secret_key,
) -> AsyncGenerator[S3Client]:
    async with S3_SESSION.client(
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
async def get_channel() -> AsyncGenerator[AbstractChannel]:
    assert connection.RABBIT_MQ_CONNECTION is not None
    async with cast(
        AbstractChannel,
        connection.RABBIT_MQ_CONNECTION.channel(),
    ) as channel:
        yield channel


@asynccontextmanager
async def get_rabbitmq_service() -> AsyncGenerator[RabbitMQService]:
    async with get_channel() as channel:
        rabbitmq_service = RabbitMQService(channel)
        yield rabbitmq_service
