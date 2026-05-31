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

    async def copy_file(self) -> None: ...

    async def delete_file(self) -> None: ...

    async def move_file(self) -> None: ...

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
