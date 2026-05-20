from datetime import datetime

from fastapi import APIRouter, status

from dependencies.annotations.cache_services import WatchHistoryCacheServiceDep
from dependencies.annotations.security import AuthUserByAccessTokenDep
from dependencies.annotations.validators import PaginationPageDep, PaginationSizeDep
from schemas.watch_history import WatchHistoryWithMovieResponseList

router = APIRouter(
    prefix="/about-me",
)


@router.get(
    "/",
    response_model=WatchHistoryWithMovieResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_watch_history_list(
    user_id: AuthUserByAccessTokenDep,
    watch_history_cache_service: WatchHistoryCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> WatchHistoryWithMovieResponseList:
    return await watch_history_cache_service.get_watch_history_list(user_id, size, page)


@router.get(
    "/by-date-range",
    response_model=WatchHistoryWithMovieResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_watch_history_by_date_range(
    user_id: AuthUserByAccessTokenDep,
    start_date: datetime,
    end_date: datetime,
    watch_history_cache_service: WatchHistoryCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> WatchHistoryWithMovieResponseList:
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
    user_id: AuthUserByAccessTokenDep,
    watch_history_cache_service: WatchHistoryCacheServiceDep,
) -> int:
    return await watch_history_cache_service.count_user_watch_history(user_id)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_watch_history(
    user_id: AuthUserByAccessTokenDep,
    watch_history_cache_service: WatchHistoryCacheServiceDep,
) -> None:
    await watch_history_cache_service.delete_user_watch_history(user_id)
