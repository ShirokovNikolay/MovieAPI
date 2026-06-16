import asyncio

from packages.celery.constants import TaskType

from core.minio.utils import get_minio_service

from .celery_app import app


@app.task(  # type: ignore[untyped-decorator]
    name=TaskType.delete_temporary_file.value,
)
def delete_temporary_file(bucket_name: str, object_name: str) -> None:
    async def async_delete_temporary_file() -> None:
        async with get_minio_service() as minio_service:
            if await minio_service.file_exists(bucket_name, object_name):
                await minio_service.delete_file(
                    bucket_name=bucket_name,
                    key=object_name,
                )

    asyncio.run(
        async_delete_temporary_file(),
    )
