import asyncio
from collections.abc import Callable, Coroutine
from typing import Any

from aio_pika import IncomingMessage
from packages.rabbitmq.constants import Exchange, ExchangeType, Queue
from packages.rabbitmq.utils import create_message, get_message

from cache_services import GenreCacheService, MovieCacheService
from core.constants import AnyPydanticType, CacheEntity
from core.utils import (
    get_cache_key_service,
    get_genre_cache_service,
    get_movie_cache_service,
    get_watch_history_redis_service,
)
from schemas.genre import GenrePartialUpdate
from schemas.movie import MoviePartialUpdate


async def update_watch_history_cache_on_watch_movie(message: IncomingMessage) -> None:
    async with (
        message.process(),
        get_watch_history_redis_service() as redis_service,
        get_cache_key_service() as cache_key_service,
    ):
        data = get_message(message=message)
        user_id = data["user_id"]
        watch_history_count_key = cache_key_service.build_item_key(
            entity=CacheEntity.watch_history,
            entity_id=user_id,
            action="get-count",
        )
        user_watch_history_pattern_coroutine = cache_key_service.build_list_regex_key(
            entity=CacheEntity.watch_history,
            action_regex="get",
            user_id=user_id,
            size="*",
            page="*",
        )
        user_watch_history_range_date_pattern_coroutine = (
            cache_key_service.build_list_key(
                entity=CacheEntity.watch_history,
                action="get",
                user_id=user_id,
                start_date="*",
                end_date="*",
                size="*",
                page="*",
            )
        )
        user_watch_history_pattern, user_watch_history_range_date_pattern = (
            await asyncio.gather(
                user_watch_history_pattern_coroutine,
                user_watch_history_range_date_pattern_coroutine,
            )
        )

        delete_watch_history_count_cache = redis_service.delete(
            key=watch_history_count_key,
        )
        delete_watch_history_cache = redis_service.delete_by_pattern(
            user_watch_history_pattern,
        )
        delete_watch_history_range_date_cache = redis_service.delete_by_pattern(
            user_watch_history_range_date_pattern,
        )
        await asyncio.gather(
            delete_watch_history_count_cache,
            delete_watch_history_cache,
            delete_watch_history_range_date_cache,
        )


def update_media_factory(
    schema: AnyPydanticType,
    service_class: Any,
    update_field_name: str,
    update_method_name: str,
    id_field_name: str,
    update_data_field_name: str,
    inner_service_attr_name: str,
) -> Callable[[IncomingMessage], Coroutine[Any, Any, None]]:
    """
    :param schema: схема для частичного обновления
    :param service_class: класс сервиса, у которого вызываем метод обновления сущности
    :param update_field_name: название обновляемого поля класса
    :param update_method_name: метод для обновления этого поля
    :param id_field_name: название поля с id внутри update_method
    :param update_data_field_name: название поля, куда передаем схему
    :param inner_service_attr_name: название поля с сервисом
    :return: функция-обработчик для rabbitmq
    """
    service_to_context_manager = {
        GenreCacheService: get_genre_cache_service,
        MovieCacheService: get_movie_cache_service,
    }
    get_service = service_to_context_manager[service_class]

    async def update_media_url_function(message: IncomingMessage) -> None:
        async with message.process(), get_service() as service:
            data = get_message(message=message)
            entity_id, object_url, updated_object_url = (
                data["entity_id"],
                data["object_url"],
                data["updated_object_url"],
            )
            partial_update_data = schema(  # type: ignore[operator]
                **{update_field_name: updated_object_url},
            )
            update_method = getattr(service, update_method_name)

            parameters = {
                id_field_name: entity_id,
                update_data_field_name: partial_update_data,
            }
            await update_method(**parameters)
            inner_service = getattr(service, inner_service_attr_name)
            rabbitmq_service = inner_service.rabbitmq_service
            exchange = await rabbitmq_service.declare_exchange(
                name=Exchange.app,
                type=ExchangeType.direct,
            )
            body = {
                "object_url": object_url,
            }
            await rabbitmq_service.publish(
                message=create_message(body=body),
                exchange=exchange,
                routing_key=Queue.delete_file.value,
            )

    return update_media_url_function


update_genre_poster_url = update_media_factory(
    schema=GenrePartialUpdate,  # type: ignore[type-var]
    service_class=GenreCacheService,
    update_field_name="preview_url",
    update_method_name="partial_update_genre",
    id_field_name="genre_id",
    update_data_field_name="update_data",
    inner_service_attr_name="genre_service",
)

update_movie_poster_url = update_media_factory(
    schema=MoviePartialUpdate,  # type: ignore[type-var]
    service_class=MovieCacheService,
    update_field_name="preview_url",
    update_method_name="partial_update_movie",
    id_field_name="movie_id",
    update_data_field_name="update_movie_data",
    inner_service_attr_name="movie_service",
)

update_movie_source_url = update_media_factory(
    schema=MoviePartialUpdate,  # type: ignore[type-var]
    service_class=MovieCacheService,
    update_field_name="source_url",
    update_method_name="partial_update_movie",
    id_field_name="movie_id",
    update_data_field_name="update_movie_data",
    inner_service_attr_name="movie_service",
)
