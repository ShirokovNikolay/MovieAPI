import json

from aio_pika import IncomingMessage, Message
from packages.rabbit_mq import connection, get_rabbit_mq_service

from config import settings
from dependencies import S3_SESSION, get_minio_client


async def copy_file(message: IncomingMessage) -> None:
    async with message.process():
        async with S3_SESSION.client(
            "s3",
            endpoint_url=settings.minio.url_minio,
            aws_access_key_id=settings.minio.access_key,
            aws_secret_access_key=settings.minio.secret_key,
        ) as client:
            async for minio_client in get_minio_client(client):
                data = json.loads(message.body.decode())
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

        channel = await connection.RABBIT_MQ_CONNECTION.channel()  # type: ignore[union-attr]
        async for rabbitmq_service in get_rabbit_mq_service(channel):
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
                message=Message(
                    body=json.dumps(body).encode(),
                ),
                exchange=exchange,
                routing_key="to_monolith",
            )


async def delete_temporary_file(message: IncomingMessage) -> None:
    async with (
        message.process(),
        S3_SESSION.client(
            "s3",
            endpoint_url=settings.minio.url_minio,
            aws_access_key_id=settings.minio.access_key,
            aws_secret_access_key=settings.minio.secret_key,
        ) as client,
    ):
        async for minio_client in get_minio_client(client):
            data = json.loads(message.body.decode())
            bucket_name, key = (
                data["bucket_name"],
                data["object_name"],
            )

            await minio_client.delete_file(
                bucket_name=bucket_name,
                key=key,
            )
