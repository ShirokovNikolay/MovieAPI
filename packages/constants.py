from enum import StrEnum


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
