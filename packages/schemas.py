from pydantic import BaseModel

from packages.constants import S3Bucket, S3ContentType


class PresignUrlCreate(BaseModel):
    bucket_name: S3Bucket
    file_name: str
    content_type: S3ContentType


class PresignUrlResponse(BaseModel):
    url: str
    path: str


class ConfirmUploadRequest(BaseModel):
    temp_path: str
    dest_path: str
