from typing import Callable, Any

from aio_pika import IncomingMessage

from cache_services import GenreCacheService, MovieCacheService
from core.constants import AnyPydanticType
from packages.constants import Exchange, ExchangeType, Queue
from packages.rabbitmq.utils import create_message, get_message

from core.rabbitmq.utils import get_genre_cache_service, get_movie_cache_service
from schemas.genre import GenrePartialUpdate


def update_media_factory(
    schema: AnyPydanticType,
    service_class: Any,
    update_field_name: str,
    update_method_name: str,
    id_field_name: str,
    update_data_field_name: str,
    inner_service_attr_name: str,
) -> Callable:
    """
    :param schema: Схема для частичного обновления
    :param service_class: Класс сервиса, у которого вызываем метод обновления сущности
    :param update_field_name: Название поля класса, которое мы собираемся обновить
    :param update_method_name: Метод для обновления этого поля
    :param id_field_name: Название поля с id внутри update_method
    :param update_data_field_name: Название поля, куда передаем схему
    :param inner_service_attr_name: Название поля с сервисом
    :return: функция-обработчик для rabbitmq
    """
    service_to_context_manager = {
        GenreCacheService: get_genre_cache_service,
        MovieCacheService: get_movie_cache_service,
    }
    get_service = service_to_context_manager[service_class]

    async def update_media_url_function(message: IncomingMessage):
        async with message.process(), get_service() as service:
            data = get_message(message=message)
            entity_id, bucket_name, object_name, new_object_url = (
                data["entity_id"],
                data["bucket_name"],
                data["object_name"],
                data["new_object_url"],
            )
            partial_update_data = schema(**{update_field_name: new_object_url})
            update_method = getattr(service, update_method_name)

            parameters = {
                id_field_name: entity_id,
                update_data_field_name: partial_update_data,
            }
            await update_method(**parameters)
            inner_service = getattr(service, inner_service_attr_name)
            rabbitmq_service = inner_service.rabbitmq_service
            exchange = await rabbitmq_service.declare_exchange(
                name=Exchange.app.value,
                type=ExchangeType.direct.value,
            )
            body = {
                "bucket_name": bucket_name,
                "object_name": object_name,
            }
            await rabbitmq_service.publish(
                message=create_message(body=body),
                exchange=exchange,
                routing_key=Queue.delete_file.value,
            )

    return update_media_url_function


update_genre_poster_url = update_media_factory(
    schema=GenrePartialUpdate,
    service_class=GenreCacheService,
    update_field_name="preview_url",
    update_method_name="partial_update_genre",
    id_field_name="genre_id",
    update_data_field_name="update_data",
    inner_service_attr_name="genre_service",
)


# async def update_genre_url(message: IncomingMessage) -> None:
#     async with message.process(), get_genre_cache_service() as genre_cache_service:
#         data = get_message(message=message)
#         genre_id, bucket_name, object_name, new_object_url = (
#             data["genre_id"],
#             data["bucket_name"],
#             data["object_name"],
#             data["new_object_url"],
#         )
#         genre_partial_update = GenrePartialUpdate(
#             preview_url=new_object_url,
#         )
#         await genre_cache_service.partial_update_genre(
#             genre_id=genre_id,
#             update_data=genre_partial_update,
#         )
#         rabbitmq_service = genre_cache_service.genre_service.rabbitmq_service
#         exchange = await rabbitmq_service.declare_exchange(
#             name=Exchange.app.value,
#             type=ExchangeType.direct.value,
#         )
#         body = {
#             "bucket_name": bucket_name,
#             "object_name": object_name,
#         }
#         await rabbitmq_service.publish(
#             message=create_message(body=body),
#             exchange=exchange,
#             routing_key=Queue.delete_file.value,
#         )
