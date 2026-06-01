import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, status
from pydantic import BaseModel

from dependencies import get_minio_service
from service import MinioService

router = APIRouter()


class ConfirmUploadRequest(BaseModel):
    temp_path: str
    dest_path: str


@router.get(
    "/presign-url",
    status_code=status.HTTP_200_OK,
)
async def get_presign_url(
    file_name: str,
    content_type: str,
    minio_service: Annotated[
        MinioService,
        Depends(get_minio_service),
    ],
) -> dict[str, str]:
    file_path = f"tmp/genre/{uuid.uuid4()}_{file_name}"
    url = await minio_service.create_presigned_url(
        bucket_name="genre-posters",
        object_name=file_path,
        expires_in=15 * 60,
        client_method="put_object",
        content_type=content_type,
    )
    return {
        "upload_url": url,
        "temp_path": file_path,
    }


@router.post(
    "/confirm-upload",
    status_code=status.HTTP_200_OK,
)
async def confirm_upload(
    payload: ConfirmUploadRequest,
    minio_service: Annotated[MinioService, Depends(get_minio_service)],
) -> None:
    await minio_service.move_file(
        bucket_name="genre-posters",
        source_path=payload.temp_path,
        destination_path=payload.dest_path,
    )


@router.post("/upload", status_code=status.HTTP_200_OK)
async def upload_file(
    file: UploadFile,
    minio_service: Annotated[
        MinioService,
        Depends(get_minio_service),
    ],
) -> None:
    file_path = f"genre/{uuid.uuid4()}_{file.filename}"
    await minio_service.upload_file(
        bucket="genre-posters",
        file=file.file,
        key=file_path,
    )
