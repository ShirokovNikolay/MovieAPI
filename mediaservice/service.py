from typing import cast
from uuid import uuid4

from fastapi import UploadFile
from packages.constants import S3Bucket
from packages.schemas import ConfirmUploadRequest, PresignUrlCreate, PresignUrlResponse

from config import settings
from minio_client import MinioClient


class MinioService:
    def __init__(self, minio_client: MinioClient) -> None:
        self.minio_client = minio_client

    @staticmethod
    def generate_name_object(file_name: str) -> str:
        temporary_prefix = settings.minio.temporary_prefix
        object_name = f"{temporary_prefix}{uuid4()}_{file_name}"
        return object_name

    async def create_presign_url(
        self,
        presign_url_create: PresignUrlCreate,
    ) -> PresignUrlResponse:
        file_name = presign_url_create.file_name
        temporary_prefix = settings.minio.temporary_prefix
        object_name = f"{temporary_prefix}{uuid4()}_{file_name}"
        presign_url = await self.minio_client.create_presign_url(
            bucket_name=presign_url_create.bucket_name,
            object_name=object_name,
            expires_in=settings.minio.expires_in,
            content_type=presign_url_create.content_type,
            client_method="put_object",
        )
        return PresignUrlResponse(
            url=presign_url.replace("minio", "localhost"),
            path=object_name,
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
        object_name = self.generate_name_object(
            file_name=cast(str, uploaded_file.filename),
        )
        await self.minio_client.upload_file(
            bucket_name=bucket_name,
            object_name=object_name,
            file=uploaded_file.file,
        )
