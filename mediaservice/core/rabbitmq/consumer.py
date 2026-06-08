from aio_pika import IncomingMessage
from packages.constants import Exchange, ExchangeType, Queue
from packages.rabbitmq.utils import create_message, get_message, get_rabbitmq_service

from core.config import settings
from core.rabbitmq.utils import get_minio_service


async def copy_file(message: IncomingMessage) -> None:
    async with message.process(), get_minio_service() as minio_service:
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

        await minio_service.copy_file(
            source_bucket_name=bucket_name,
            destination_bucket_name=bucket_name,
            source_object_name=object_name,
            destination_object_name=new_object_name,
        )

        async with get_rabbitmq_service() as rabbitmq_service:
            exchange = await rabbitmq_service.declare_exchange(
                name=Exchange.mediaservice.value,
                type=ExchangeType.direct.value,
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
                routing_key=Queue.update_genre_url.value,
            )


async def delete_temporary_file(message: IncomingMessage) -> None:
    async with message.process(), get_minio_service() as minio_service:
        data = get_message(message)
        bucket_name, key = (
            data["bucket_name"],
            data["object_name"],
        )

        await minio_service.delete_file(
            bucket_name=bucket_name,
            key=key,
        )
