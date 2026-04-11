from typing import Annotated

from fastapi import Depends, APIRouter
from starlette import status

from dependencies.auth import get_admin_by_access_token
from dependencies.services import get_watch_history_service
from schemas.watch_history import WatchHistoryResponse
from services.watch_history import WatchHistoryService

router = APIRouter(prefix="/{watch_history_id}")


@router.get(
    "/",
    response_model=WatchHistoryResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(get_admin_by_access_token),
    ],
)
async def get_watch_history_by_id(
    watch_history_id: int,
    watch_history_service: Annotated[
        WatchHistoryService,
        Depends(get_watch_history_service),
    ],
):
    return await watch_history_service.get_watch_history_by_id(watch_history_id)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(get_admin_by_access_token),
    ],
)
async def delete_watch_history_by_id(
    watch_history_id: int,
    watch_history_service: Annotated[
        WatchHistoryService,
        Depends(get_watch_history_service),
    ],
):
    await watch_history_service.delete_watch_history_by_id(watch_history_id)
