import json

from aio_pika import IncomingMessage, Message
from packages.rabbit_mq import connection, get_rabbit_mq_service

from core.constants import BASE_MINIO_URL
from core.database import session_factory
from dependencies.services import get_genre_service
from schemas.genre import GenrePartialUpdate


async def update_genre_url(message: IncomingMessage) -> None:
    async with message.process():
        # print("updating genre url")
        channel = await connection.RABBIT_MQ_CONNECTION.channel()  # type: ignore[union-attr]
        async for rabbitmq_service in get_rabbit_mq_service(channel):
            async for genre_service in get_genre_service(
                session=session_factory(),
                rabbitmq=rabbitmq_service,
            ):
                data = json.loads(message.body.decode())
                genre_id, bucket_name, object_name, new_object_name = (
                    data["genre_id"],
                    data["bucket_name"],
                    data["object_name"],
                    data["new_object_name"],
                )
                genre_partial_update = GenrePartialUpdate(
                    preview_url=BASE_MINIO_URL + "/genre-posters/" + new_object_name,
                )
                # print("New object name:", new_object_name)
                await genre_service.partial_update_genre(
                    genre_id=genre_id,
                    update_data=genre_partial_update,
                )

            exchange = await rabbitmq_service.declare_exchange(
                name="to_mediaservice",
                type="direct",
            )
            body = {
                "object_name": object_name,
                "bucket_name": bucket_name,
            }
            await rabbitmq_service.publish(
                message=Message(
                    body=json.dumps(body).encode(),
                ),
                exchange=exchange,
                routing_key="to_mediaservice",
            )
