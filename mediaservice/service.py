from typing import BinaryIO

from types_aiobotocore_s3 import S3Client


class MinioService:
    def __init__(
        self,
        client: S3Client,
    ) -> None:
        self.s3_client = client

    async def create_presigned_url(
        self,
        bucket_name: str,
        object_name: str,
        expires_in: int,
        client_method: str,
        content_type: str,
    ) -> str:
        return await self.s3_client.generate_presigned_url(
            ClientMethod=client_method,
            ExpiresIn=expires_in,
            Params={
                "Bucket": bucket_name,
                "Key": object_name,
                "ContentType": content_type,
            },
        )

    async def copy_file(
        self,
        bucket: str,
        source_path: str,
        destination_path: str,
    ) -> None:
        copy_source = {"Bucket": bucket, "Key": source_path}
        await self.s3_client.copy_object(
            Bucket=bucket,
            CopySource=copy_source,  # type: ignore[arg-type]
            Key=destination_path,
        )

    async def delete_file(self, bucket: str, key: str) -> None:
        await self.s3_client.delete_object(Bucket=bucket, Key=key)

    async def move_file(
        self,
        bucket_name: str,
        source_path: str,
        destination_path: str,
    ) -> None:
        await self.copy_file(bucket_name, source_path, destination_path)
        await self.delete_file(bucket_name, source_path)

    async def upload_file(
        self,
        bucket: str,
        key: str,
        file: BinaryIO,
    ) -> None:
        await self.s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=file,
        )
