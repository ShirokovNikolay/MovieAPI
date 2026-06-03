from pydantic import BaseModel

from packages.constants import S3Bucket, S3ContentType


class PresignUrlCreate(BaseModel):
    """
    Модель для создания временной ссылки доступа к хранилищу S3.
    """

    bucket_name: S3Bucket
    file_name: str
    content_type: S3ContentType


class PresignUrlResponse(BaseModel):
    """
    Модель для вывода информации о временной ссылке доступа к хранилищу S3.
    """

    url: str
    path: str


class ConfirmUploadRequest(BaseModel):
    """
    Модель для подтверждения корректности загрузки файла и последующего
    переноса файла в основную директорию.
    """

    source_bucket_name: S3Bucket
    destination_bucket_name: S3Bucket
    source_object_name: str
    destination_object_name: str
