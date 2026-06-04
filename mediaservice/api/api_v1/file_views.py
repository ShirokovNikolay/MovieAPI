from fastapi import APIRouter, UploadFile, status
from packages.constants import S3Bucket
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
    status_code=status.HTTP_201_CREATED,
)
async def create_presign_url(
    presign_url_create: PresignUrlCreate,
    minio_service: MinioServiceDep,
) -> PresignUrlResponse:
    return await minio_service.create_presign_url(presign_url_create)


@router.post(
    "/confirm-upload-file",
    status_code=status.HTTP_200_OK,
)
async def confirm_upload_file(
    confirm_upload_payload: ConfirmUploadRequest,
    minio_service: MinioServiceDep,
) -> None:
    await minio_service.confirm_upload_file(
        confirm_upload_payload=confirm_upload_payload,
    )


@router.post(
    "/upload-file",
    status_code=status.HTTP_200_OK,
)
async def upload_file(
    bucket_name: S3Bucket,
    uploaded_file: UploadFile,
    minio_service: MinioServiceDep,
) -> None:
    await minio_service.upload_file(
        uploaded_file=uploaded_file,
        bucket_name=bucket_name,
    )
