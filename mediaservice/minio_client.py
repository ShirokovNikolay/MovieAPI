from typing import BinaryIO

from types_aiobotocore_s3 import S3Client


class MinioClient:
    def __init__(
        self,
        client: S3Client,
    ) -> None:
        self.s3_client = client

    async def create_presign_url(
        self,
        bucket_name: str,
        object_name: str,
        expires_in: int,
        client_method: str,
        content_type: str,
    ) -> str:
        params = {
            "Bucket": bucket_name,
            "Key": object_name,
            "ContentType": content_type,
        }
        return await self.s3_client.generate_presigned_url(
            ClientMethod=client_method,
            ExpiresIn=expires_in,
            Params=params,
        )

    async def copy_file(
        self,
        source_bucket_name: str,
        destination_bucket_name: str,
        source_object_name: str,
        destination_object_name: str,
    ) -> None:
        copy_source = {
            "Bucket": source_bucket_name,
            "Key": source_object_name,
        }
        await self.s3_client.copy_object(
            Bucket=destination_bucket_name,
            CopySource=copy_source,  # type: ignore[arg-type]
            Key=destination_object_name,
        )

    async def delete_file(self, bucket: str, key: str) -> None:
        await self.s3_client.delete_object(
            Bucket=bucket,
            Key=key,
        )

    async def move_file(
        self,
        source_bucket_name: str,
        destination_bucket_name: str,
        source_object_name: str,
        destination_object_name: str,
    ) -> None:
        await self.copy_file(
            source_bucket_name,
            destination_bucket_name,
            source_object_name,
            destination_object_name,
        )
        await self.delete_file(source_bucket_name, source_object_name)

    async def upload_file(
        self,
        bucket_name: str,
        object_name: str,
        file: BinaryIO,
    ) -> None:
        await self.s3_client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=file,
        )
