from typing import cast

from core.redis.cache_service import CacheService
from schemas.user import (
    UserCreate,
    UserLogin,
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
        cache_service: CacheService,
    ) -> None:
        self.user_service = user_service
        self.cache_service = cache_service

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        key = CacheService.create_cache_key("user", user_id=user_id)
        cached_user_response = await self.cache_service.get(key, UserResponse)
        if cached_user_response is not None:
            return cast(UserResponse, cached_user_response)

        user_response = await self.user_service.get_user_by_id(user_id)
        await self.cache_service.set(key, user_response)
        return user_response

    async def get_user_by_login(self, login: str) -> UserResponse:
        key = CacheService.create_cache_key("user", login=login)
        cached_user_response = await self.cache_service.get(key, UserResponse)
        if cached_user_response is not None:
            return cast(UserResponse, cached_user_response)

        user_response = await self.user_service.get_user_by_login(login)
        await self.cache_service.set(key, user_response)
        return user_response

    async def get_all_users(self, size: int = 10, page: int = 1) -> UserResponseList:
        key = CacheService.create_cache_key("users", size=size, page=page)
        cached_users_response = await self.cache_service.get(key, UserResponseList)
        if cached_users_response is not None:
            return cast(UserResponseList, cached_users_response)

        users_response = await self.user_service.get_all_users(size, page)
        await self.cache_service.set(key, users_response)
        return users_response

    async def create_user(self, create_user_data: UserCreate) -> UserResponse:
        user_response = await self.user_service.create_user(create_user_data)
        key = CacheService.create_cache_key("user")
        pattern = key + "*"
        await self.cache_service.delete_by_pattern(pattern)
        return user_response

    async def update_user(
        self,
        user_id: int,
        update_data: UserUpdate,
    ) -> UserResponse:
        user_response = await self.user_service.update_user(user_id, update_data)
        key = CacheService.create_cache_key("user")
        pattern = key + "*"
        await self.cache_service.delete_by_pattern(pattern)
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
        key = CacheService.create_cache_key("user")
        pattern = key + "*"
        await self.cache_service.delete_by_pattern(pattern)
        return user_response

    async def delete_user_by_id(self, user_id: int) -> None:
        await self.user_service.delete_user_by_id(user_id)
        key = CacheService.create_cache_key("user")
        pattern = key + "*"
        await self.cache_service.delete_by_pattern(pattern)

    async def delete_user_by_login(self, login: str) -> None:
        await self.user_service.delete_user_by_login(login)
        key = CacheService.create_cache_key("user")
        pattern = key + "*"
        await self.cache_service.delete_by_pattern(pattern)

    async def authenticate_user(self, login_data: UserLogin) -> UserResponse:
        key = CacheService.create_cache_key(
            "user",
            login=login_data.login,
            password=login_data.password,
        )
        cached_user_response = await self.cache_service.get(key, UserResponse)
        if cached_user_response is not None:
            return cast(UserResponse, cached_user_response)

        user_response = await self.user_service.authenticate_user(login_data)
        await self.cache_service.set(key, user_response)
        return user_response
