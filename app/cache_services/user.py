import asyncio
from typing import cast

from packages.celery.constants import Queue, TaskType

from core.celery.celery_app import app
from core.constants import CacheEntity
from core.redis.cache_key_service import CacheKeyService
from core.redis.service import RedisService
from schemas.user import (
    UserCreate,
    UserPartialUpdate,
    UserResponse,
    UserResponseList,
    UserUpdate,
)
from services import UserService


class UserCacheService:
    def __init__(
        self,
        user_service: UserService,
        redis_service: RedisService,
        cache_key_service: CacheKeyService,
    ) -> None:
        self.user_service = user_service
        self.redis_service = redis_service
        self.cache_key_service = cache_key_service

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        key = self.cache_key_service.build_item_key(
            entity=CacheEntity.user,
            entity_id=user_id,
            action="get",
        )
        cached_user_response = await self.redis_service.get(key, UserResponse)
        if cached_user_response is not None:
            return cast(UserResponse, cached_user_response)

        user_response = await self.user_service.get_user_by_id(user_id)
        await self.redis_service.set(
            key,
            user_response,
            ttl=24 * 60 * 60,
        )
        return user_response

    async def get_user_by_login(self, login: str) -> UserResponse:
        key = self.cache_key_service.build_item_key(
            entity=CacheEntity.user,
            entity_id=login,
            action="get-by-login",
        )
        cached_user_response = await self.redis_service.get(key, UserResponse)
        if cached_user_response is not None:
            return cast(UserResponse, cached_user_response)

        user_response = await self.user_service.get_user_by_login(login)
        await self.redis_service.set(
            key,
            user_response,
            ttl=24 * 60 * 60,
        )
        return user_response

    async def get_all_users(self, size: int = 10, page: int = 1) -> UserResponseList:
        key = await self.cache_key_service.build_list_key(
            entity=CacheEntity.user,
            action="get",
            size=size,
            page=page,
        )
        cached_users_response = await self.redis_service.get(key, UserResponseList)
        if cached_users_response is not None:
            return cast(UserResponseList, cached_users_response)

        users_response = await self.user_service.get_all_users(size, page)
        await self.redis_service.set(
            key,
            users_response,
            ttl=12 * 60 * 60,
        )
        return users_response

    async def create_user(
        self,
        user_create_data: UserCreate,
    ) -> UserResponse:
        user_response = await self.user_service.create_user(user_create_data)
        await self.cache_key_service.invalidate_list_keys(entity=CacheEntity.user)
        return user_response

    async def update_user(
        self,
        user_id: int,
        update_data: UserUpdate,
    ) -> UserResponse:
        user_response = await self.user_service.update_user(user_id, update_data)
        user_key = self.cache_key_service.build_item_key(
            entity=CacheEntity.user,
            entity_id=user_id,
            action="get",
        )
        await asyncio.gather(
            self.redis_service.delete(user_key),
            self.cache_key_service.invalidate_list_keys(entity=CacheEntity.user),
        )
        app.send_task(
            args=[user_id],
            name=TaskType.invalidate_reviews_cache_on_update_user.value,
            queue=Queue.app.value,
        )
        return user_response

    async def partial_update_user(
        self,
        user_id: int,
        update_data: UserPartialUpdate,
    ) -> UserResponse:
        user_response = await self.user_service.partial_update_user(
            user_id,
            update_data,
        )
        user_key = self.cache_key_service.build_item_key(
            entity=CacheEntity.user,
            entity_id=user_id,
            action="get",
        )
        await asyncio.gather(
            self.redis_service.delete(user_key),
            self.cache_key_service.invalidate_list_keys(entity=CacheEntity.user),
        )
        app.send_task(
            args=[user_id],
            name=TaskType.invalidate_reviews_cache_on_update_user.value,
            queue=Queue.app.value,
        )
        return user_response

    async def delete_user_by_id(self, user_id: int) -> None:
        await self.user_service.delete_user_by_id(user_id)
        user_key = self.cache_key_service.build_item_key(
            entity=CacheEntity.user,
            entity_id=user_id,
            action="get",
        )
        await asyncio.gather(
            self.redis_service.delete(user_key),
            self.cache_key_service.invalidate_list_keys(entity=CacheEntity.user),
        )
        app.send_task(
            args=[user_id],
            name=TaskType.invalidate_reviews_cache_on_update_user.value,
            queue=Queue.app.value,
        )

    async def delete_user_by_login(self, login: str) -> None:
        await self.user_service.delete_user_by_login(login)
        user_key = self.cache_key_service.build_item_key(
            entity=CacheEntity.user,
            entity_id=login,
            action="get-by-login",
        )
        await asyncio.gather(
            self.redis_service.delete(user_key),
            self.cache_key_service.invalidate_list_keys(entity=CacheEntity.user),
        )
