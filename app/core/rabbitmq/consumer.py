from aio_pika import IncomingMessage
from packages.constants import Exchange, ExchangeType, Queue
from packages.rabbitmq.utils import create_message, get_message

from core.constants import BASE_MINIO_URL
from core.rabbitmq.utils import get_genre_cache_service
from schemas.genre import GenrePartialUpdate


async def update_genre_url(message: IncomingMessage) -> None:
    async with message.process(), get_genre_cache_service() as genre_cache_service:
        data = get_message(message=message)
        genre_id, bucket_name, object_name, new_object_name = (
            data["genre_id"],
            data["bucket_name"],
            data["object_name"],
            data["new_object_name"],
        )
        genre_partial_update = GenrePartialUpdate(
            preview_url=BASE_MINIO_URL + "/genre-posters/" + new_object_name,
        )
        await genre_cache_service.partial_update_genre(
            genre_id=genre_id,
            update_data=genre_partial_update,
        )
        rabbitmq_service = genre_cache_service.genre_service.rabbitmq_service
        exchange = await rabbitmq_service.declare_exchange(
            name=Exchange.app.value,
            type=ExchangeType.direct.value,
        )
        body = {
            "object_name": object_name,
            "bucket_name": bucket_name,
        }
        await rabbitmq_service.publish(
            message=create_message(body=body),
            exchange=exchange,
            routing_key=Queue.delete_file.value,
        )
