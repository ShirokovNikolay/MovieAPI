import uuid
from enum import StrEnum
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, status
from pydantic import BaseModel

from dependencies import get_minio_service
from service import MinioService

router = APIRouter()


class ConfirmUploadRequest(BaseModel):
    temp_path: str
    dest_path: str


class S3Bucket(StrEnum):
    genre_posters = "genre-posters"
    movie_posters = "movie-posters"
    movies = "movies"


class S3ContentType(StrEnum):
    jpeg = "image/jpeg"
    jpg = "image/jpg"
    pngr = "image/png"
    webp = "image/webp"
    mp4 = "video/mp4"


class CreatePresignedUrlRequest(BaseModel):
    bucket_name: S3Bucket
    file_name: str
    content_type: S3ContentType


class PresignUrlResponse(BaseModel):
    url: str
    path: str


MinioServiceDep = Annotated[
    MinioService,
    Depends(get_minio_service),
]


@router.post(
    "/presign-url",
    status_code=status.HTTP_200_OK,
)
async def get_presign_url(
    presign_request: CreatePresignedUrlRequest,
    minio_service: MinioServiceDep,
) -> PresignUrlResponse:
    file_path = f"tmp/genre/{uuid.uuid4()}_{presign_request.file_name}"
    url = await minio_service.create_presigned_url(
        bucket_name=presign_request.bucket_name.value,
        object_name=file_path,
        expires_in=15 * 60,
        client_method="put_object",
        content_type=presign_request.content_type.value,
    )
    return PresignUrlResponse(
        url=url,
        path=file_path,
    )


@router.post(
    "/confirm-upload",
    status_code=status.HTTP_200_OK,
)
async def confirm_upload(
    payload: ConfirmUploadRequest,
    minio_service: MinioServiceDep,
) -> None:
    await minio_service.move_file(
        bucket_name="genre-posters",
        source_path=payload.temp_path,
        destination_path=payload.dest_path,
    )


@router.post(
    "/upload",
    status_code=status.HTTP_200_OK,
)
async def upload_file(
    file: UploadFile,
    minio_service: MinioServiceDep,
) -> None:
    file_path = f"genre/{uuid.uuid4()}_{file.filename}"
    await minio_service.upload_file(
        bucket_name="genre-posters",
        file=file.file,
        key=file_path,
    )
