from enum import StrEnum


class ActionType(StrEnum):
    update_genre_url = "update_genre_url"
    copy_file = "copy_file"
    delete_file = "delete_file"


class ExchangeType(StrEnum):
    direct = "direct"
    fanout = "fanout"
    topic = "topic"
    headers = "headers"


def create_exchange_name(
    producer: str,
    entity: str,
    exchange_type: ExchangeType,
) -> str:
    exchange_name = f"{producer}.{entity}.{exchange_type.value}"
    return exchange_name


def create_queue_name(
    consumer: str,
    entity: str,
    action: ActionType,
) -> str:
    queue_name = f"{consumer}.{entity}.{action.value}"
    return queue_name


class S3Bucket(StrEnum):
    genre_posters = "genre-posters"
    movie_posters = "movie-posters"
    movies = "movies"


class S3ContentType(StrEnum):
    image_jpeg = "image/jpeg"
    image_jpg = "image/jpg"
    image_png = "image/png"
    image_webp = "image/webp"
    video_mp4 = "video/mp4"


class S3ClientMethod(StrEnum):
    get_objects = "get_object"
    put_object = "put_object"
    copy_object = "copy_object"
    delete_object = "delete_object"
    delete_objects = "delete_objects"


class Exchange(StrEnum):
    app = create_exchange_name(
        producer="app",
        entity="content",
        exchange_type=ExchangeType.direct,
    )
    mediaservice = create_exchange_name(
        "mediaservice",
        entity="content",
        exchange_type=ExchangeType.direct,
    )


class Queue(StrEnum):
    update_genre_url = create_queue_name(
        consumer="app",
        entity="content",
        action=ActionType.update_genre_url,
    )
    copy_file = create_queue_name(
        consumer="mediaservice",
        entity="content",
        action=ActionType.copy_file,
    )
    delete_file = create_queue_name(
        consumer="mediaservice",
        entity="content",
        action=ActionType.delete_file,
    )
