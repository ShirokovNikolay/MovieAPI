from aio_pika import IncomingMessage
from packages.constants import S3Bucket
from packages.rabbitmq.constants import Exchange, ExchangeType, Queue
from packages.rabbitmq.utils import create_message, get_message, get_rabbitmq_service

from core.config import settings
from core.minio.utils import get_minio_service


async def copy_file(message: IncomingMessage) -> None:
    async with message.process(), get_minio_service() as minio_service:
        data = get_message(message)
        entity_id, object_url = data["entity_id"], data["object_url"]

        bucket_name = minio_service.get_bucket_name_from_url(object_url)
        object_name = minio_service.get_object_name_from_url(object_url)
        destination_object_name = object_name.replace(
            settings.minio.temporary_prefix,
            "",
        )
        prefix_url = settings.minio.url_minio.replace("minio", "localhost")
        updated_object_url_list = [prefix_url, bucket_name, destination_object_name]
        updated_object_url = "/".join(updated_object_url_list)

        await minio_service.copy_file(
            source_bucket_name=bucket_name,
            destination_bucket_name=bucket_name,
            source_object_name=object_name,
            destination_object_name=destination_object_name,
        )

        async with get_rabbitmq_service() as rabbitmq_service:
            exchange = await rabbitmq_service.declare_exchange(
                name=Exchange.mediaservice,
                type=ExchangeType.direct,
                durable=True,
            )
            body = {
                "entity_id": entity_id,
                "object_url": object_url,
                "updated_object_url": updated_object_url,
            }
            get_routing_key_by_bucket = {
                S3Bucket.genre_posters.value: Queue.update_genre_poster_url.value,
                S3Bucket.movie_posters.value: Queue.update_movie_poster_url.value,
                S3Bucket.movies.value: Queue.update_movie_source_url.value,
            }
            routing_key = get_routing_key_by_bucket[bucket_name]
            await rabbitmq_service.publish(
                message=create_message(body=body),
                exchange=exchange,
                routing_key=routing_key,
            )


async def delete_file(message: IncomingMessage) -> None:
    async with message.process(), get_minio_service() as minio_service:
        data = get_message(message)
        object_url = data["object_url"]
        bucket_name = minio_service.get_bucket_name_from_url(object_url)
        object_name = minio_service.get_object_name_from_url(object_url)
        await minio_service.delete_file(
            bucket_name=bucket_name,
            key=object_name,
        )
