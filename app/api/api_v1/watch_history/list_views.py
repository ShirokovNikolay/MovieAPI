from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, status, Depends, Query

from cache_services.watch_history import WatchHistoryCacheService
from dependencies.auth import get_user_by_access_token
from dependencies.cache_services import get_watch_history_cache_service
from dependencies.services import get_watch_history_service
from schemas.watch_history import WatchHistoryResponseList
from services.watch_history import WatchHistoryService

router = APIRouter(
    prefix="/about-me",
)


@router.get(
    "/",
    response_model=WatchHistoryResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_watch_history_list(
    user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    watch_history_cache_service: Annotated[
        WatchHistoryCacheService,
        Depends(get_watch_history_cache_service),
    ],
    size: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
):
    return await watch_history_cache_service.get_watch_history_list(user_id, size, page)


@router.get(
    "/range-by-time",
    response_model=WatchHistoryResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_watch_history_by_date_range(
    user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    start_date: datetime,
    end_date: datetime,
    watch_history_cache_service: Annotated[
        WatchHistoryCacheService,
        Depends(get_watch_history_cache_service),
    ],
    size: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
):
    return await watch_history_cache_service.get_watch_history_by_date_range(
        user_id,
        start_date,
        end_date,
        size,
        page,
    )


@router.get(
    "/count",
    status_code=status.HTTP_200_OK,
)
async def count_user_watch_history(
    user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    watch_history_cache_service: Annotated[
        WatchHistoryCacheService,
        Depends(get_watch_history_cache_service),
    ],
):
    return await watch_history_cache_service.count_user_watch_history(user_id)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_watch_history(
    user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    watch_history_cache_service: Annotated[
        WatchHistoryCacheService,
        Depends(get_watch_history_cache_service),
    ],
):
    await watch_history_cache_service.delete_user_watch_history(user_id)
