from enum import StrEnum

from packages.rabbitmq.utils import create_exchange_name, create_queue_name


class ConsumerType(StrEnum):
    app = "app"
    media_service = "media-service"
    notification_service = "notification-service"


class ProducerType(StrEnum):
    app = "app"
    media_service = "media-service"
    notification_service = "notification-service"


class ActionType(StrEnum):
    update_genre_poster_url = "update_genre_poster_url"
    update_movie_poster_url = "update_movie_poster_url"
    update_movie_source_url = "update_movie_source_url"
    copy_file = "copy_file"
    delete_file = "delete_file"

    update_watch_history_cache_on_watch_movie = (
        "update_watch_history_cache_on_watch_movie"
    )


class ExchangeType(StrEnum):
    direct = "direct"
    fanout = "fanout"
    topic = "topic"
    headers = "headers"


class Exchange(StrEnum):
    app = create_exchange_name(
        producer=ProducerType.app,
        entity="content",
        exchange_type=ExchangeType.direct,
    )
    media_service = create_exchange_name(
        producer=ProducerType.media_service,
        entity="content",
        exchange_type=ExchangeType.direct,
    )


class Queue(StrEnum):
    update_genre_poster_url = create_queue_name(
        consumer=ConsumerType.app,
        entity="content",
        action=ActionType.update_genre_poster_url,
    )
    update_movie_poster_url = create_queue_name(
        consumer=ConsumerType.app,
        entity="content",
        action=ActionType.update_movie_poster_url,
    )
    update_movie_source_url = create_queue_name(
        consumer=ConsumerType.app,
        entity="content",
        action=ActionType.update_movie_source_url,
    )
    copy_file = create_queue_name(
        consumer=ConsumerType.media_service,
        entity="content",
        action=ActionType.copy_file,
    )
    delete_file = create_queue_name(
        consumer=ConsumerType.media_service,
        entity="content",
        action=ActionType.delete_file,
    )

    update_watch_history_cache_on_watch_movie = create_queue_name(
        consumer=ConsumerType.app,
        entity="content",
        action=ActionType.update_watch_history_cache_on_watch_movie,
    )
