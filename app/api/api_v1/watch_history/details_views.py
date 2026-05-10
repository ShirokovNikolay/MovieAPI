from fastapi import APIRouter, Depends
from starlette import status

from dependencies.annotations.cache_services import WatchHistoryCacheServiceDep
from dependencies.annotations.security import AuthUserByAccessTokenDep
from dependencies.auth import get_admin_by_access_token
from schemas.watch_history import WatchHistoryWithMovieResponse

router = APIRouter(
    prefix="/{watch_history_id}",
)


@router.get(
    "/",
    response_model=WatchHistoryWithMovieResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(get_admin_by_access_token),
    ],
)
async def get_watch_history_by_id(
    watch_history_id: int,
    watch_history_cache_service: WatchHistoryCacheServiceDep,
) -> WatchHistoryWithMovieResponse:
    return await watch_history_cache_service.get_watch_history_by_id(watch_history_id)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_watch_history_by_id(
    watch_history_id: int,
    user_id: AuthUserByAccessTokenDep,
    watch_history_cache_service: WatchHistoryCacheServiceDep,
) -> None:
    await watch_history_cache_service.delete_watch_history_by_id(
        user_id,
        watch_history_id,
    )
