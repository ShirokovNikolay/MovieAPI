from typing import cast
from urllib.parse import urlsplit
from uuid import uuid4

from fastapi import UploadFile
from packages.celery.constants import Queue, TaskType
from packages.constants import S3Bucket
from packages.schemas import ConfirmUploadRequest, PresignUrlCreate, PresignUrlResponse

from core.celery.celery_app import app
from core.config import settings
from core.minio.client import MinioClient


class MinioService:
    def __init__(self, minio_client: MinioClient) -> None:
        self.minio_client = minio_client

    @staticmethod
    def generate_object_name(
        file_name: str,
        prefix_object_name: str = "",
    ) -> str:
        object_name = f"{prefix_object_name}{uuid4()}_{file_name}"
        return object_name

    async def create_presign_url(
        self,
        presign_url_create: PresignUrlCreate,
    ) -> PresignUrlResponse:
        object_name = self.generate_object_name(
            file_name=presign_url_create.file_name,
            prefix_object_name=settings.minio.temporary_prefix,
        )
        presign_url = await self.minio_client.create_presign_url(
            bucket_name=presign_url_create.bucket_name,
            object_name=object_name,
            expires_in=settings.minio.expires_in,
            content_type=presign_url_create.content_type,
            client_method=presign_url_create.client_method,
        )

        app.send_task(
            name=TaskType.delete_temporary_file.value,
            args=[
                presign_url_create.bucket_name.value,
                object_name,
            ],
            countdown=settings.celery.delete_temporary_file_in,
            queue=Queue.mediaservice.value,
        )
        return PresignUrlResponse(
            presign_url=presign_url.replace("minio", "localhost"),
            temporary_path=object_name,
        )

    async def confirm_upload_file(
        self,
        confirm_upload_payload: ConfirmUploadRequest,
    ) -> None:
        await self.minio_client.move_file(
            source_bucket_name=confirm_upload_payload.source_bucket_name,
            destination_bucket_name=confirm_upload_payload.destination_bucket_name,
            source_object_name=confirm_upload_payload.source_object_name,
            destination_object_name=confirm_upload_payload.destination_object_name,
        )

    async def upload_file(
        self,
        bucket_name: S3Bucket,
        uploaded_file: UploadFile,
    ) -> None:
        object_name = self.generate_object_name(
            file_name=cast(str, uploaded_file.filename),
        )
        await self.minio_client.upload_file(
            bucket_name=bucket_name,
            object_name=object_name,
            file=uploaded_file.file,
        )

    async def copy_file(
        self,
        source_bucket_name: str,
        destination_bucket_name: str,
        source_object_name: str,
        destination_object_name: str,
    ) -> None:
        if (
            source_bucket_name == destination_bucket_name
            and source_object_name == destination_object_name
        ):
            return

        await self.minio_client.copy_file(
            source_bucket_name=source_bucket_name,
            destination_bucket_name=destination_bucket_name,
            source_object_name=source_object_name,
            destination_object_name=destination_object_name,
        )

    async def delete_file(self, bucket_name: str, key: str) -> None:
        await self.minio_client.delete_file(
            bucket_name=bucket_name,
            key=key,
        )

    async def move_file(
        self,
        source_bucket_name: str,
        destination_bucket_name: str,
        source_object_name: str,
        destination_object_name: str,
    ) -> None:
        await self.minio_client.move_file(
            source_bucket_name=source_bucket_name,
            destination_bucket_name=destination_bucket_name,
            source_object_name=source_object_name,
            destination_object_name=destination_object_name,
        )

    async def file_exists(
        self,
        bucket_name: str,
        object_name: str,
    ) -> bool:
        return await self.minio_client.file_exists(
            bucket_name=bucket_name,
            object_name=object_name,
        )

    @classmethod
    def get_bucket_name_from_url(cls, object_url: str) -> str:
        parsed_url = urlsplit(object_url)
        path_url = parsed_url.path
        bucket_name = path_url.split("/")[1]
        return bucket_name

    @classmethod
    def get_object_name_from_url(cls, object_url: str) -> str:
        parsed_url = urlsplit(object_url)
        path_url = parsed_url.path
        object_name_list = path_url.split("/")[2:]
        object_name = "/".join(object_name_list)
        return object_name
