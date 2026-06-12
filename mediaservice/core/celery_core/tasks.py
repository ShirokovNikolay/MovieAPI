import asyncio

from .celery_app import app

from ..rabbitmq.utils import get_minio_service


@app.task
def delete_temporary_file(bucket_name: str, object_name: str) -> None:
    async def callback() -> None:
        async with get_minio_service() as minio_service:
            if await minio_service.file_exists(bucket_name, object_name):
                await minio_service.delete_file(
                    bucket_name=bucket_name,
                    key=object_name,
                )

    asyncio.run(callback())
