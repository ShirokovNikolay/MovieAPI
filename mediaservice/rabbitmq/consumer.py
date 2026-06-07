from aio_pika import IncomingMessage
from packages.rabbit_mq.utils import create_message, get_message

from config import settings
from rabbitmq.utils import get_minio_client, get_rabbitmq_service


async def copy_file(message: IncomingMessage) -> None:
    async with message.process(), get_minio_client() as minio_client:
        data = get_message(message)
        genre_id, object_name, bucket_name = (
            data["genre_id"],
            data["object_name"],
            data["bucket_name"],
        )

        object_name = object_name.replace("genre-posters/", "")
        new_object_name = object_name.replace(
            settings.minio.temporary_prefix,
            "",
        )

        await minio_client.copy_file(
            source_bucket_name=bucket_name,
            destination_bucket_name=bucket_name,
            source_object_name=object_name,
            destination_object_name=new_object_name,
        )

        async with get_rabbitmq_service() as rabbitmq_service:
            exchange = await rabbitmq_service.declare_exchange(
                name="to_monolith",
                type="direct",
                durable=True,
            )
            body = {
                "genre_id": genre_id,
                "bucket_name": bucket_name,
                "object_name": object_name,
                "new_object_name": new_object_name,
            }
            await rabbitmq_service.publish(
                message=create_message(body=body),
                exchange=exchange,
                routing_key="to_monolith",
            )


async def delete_temporary_file(message: IncomingMessage) -> None:
    async with message.process(), get_minio_client() as minio_client:
        data = get_message(message)
        bucket_name, key = (
            data["bucket_name"],
            data["object_name"],
        )

        await minio_client.delete_file(
            bucket_name=bucket_name,
            key=key,
        )
