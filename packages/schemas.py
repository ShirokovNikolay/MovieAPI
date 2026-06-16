from pydantic import BaseModel, EmailStr

from packages.constants import S3Bucket, S3ClientMethod, S3ContentType


class PresignUrlCreate(BaseModel):
    """
    Модель для создания временной ссылки доступа к хранилищу S3.
    """

    bucket_name: S3Bucket
    file_name: str
    client_method: S3ClientMethod
    content_type: S3ContentType | None = None


class PresignUrlResponse(BaseModel):
    """
    Модель для вывода информации о временной ссылке доступа к хранилищу S3.
    """

    presign_url: str
    temporary_path: str


class ConfirmUploadRequest(BaseModel):
    """
    Модель для подтверждения корректности загрузки файла и последующего
    переноса файла в основную директорию.
    """

    source_bucket_name: S3Bucket
    destination_bucket_name: S3Bucket
    source_object_name: str
    destination_object_name: str


class SendEmail(BaseModel):
    """
    Модель для отправки сообщения на почту.
    """

    subject: str
    to_email: EmailStr
    body: str
