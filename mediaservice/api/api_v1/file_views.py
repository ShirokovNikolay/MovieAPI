import uuid

from fastapi import APIRouter, UploadFile, status
from packages.schemas import (
    ConfirmUploadRequest,
    PresignUrlCreate,
    PresignUrlResponse,
)

from dependencies import MinioServiceDep

router = APIRouter()


@router.post(
    "/presign-url",
    response_model=PresignUrlResponse,
    status_code=status.HTTP_200_OK,
)
async def get_presign_url(
    presign_request: PresignUrlCreate,
    minio_service: MinioServiceDep,
) -> PresignUrlResponse:
    file_path = f"tmp/{uuid.uuid4()}_{presign_request.file_name}"
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
