import asyncio
from typing import cast

from core.constants import CacheEntity
from core.redis.cache_key_service import CacheKeyService
from core.redis.service import RedisService
from dependencies.annotations.validators import PaginationPageDep, PaginationSizeDep
from schemas.review import (
    ReviewCreate,
    ReviewPartialUpdate,
    ReviewResponse,
    ReviewUpdate,
    ReviewWithMovieResponseList,
    ReviewWithUserResponse,
    ReviewWithUserResponseList,
)
from services import ReviewService


class ReviewCacheService:
    def __init__(
        self,
        review_service: ReviewService,
        cache_service: RedisService,
        cache_key_service: CacheKeyService,
    ) -> None:
        self.review_service = review_service
        self.cache_service = cache_service
        self.cache_key_service = cache_key_service

    async def get_reviews(
        self,
        size: int = 10,
        page: int = 1,
    ) -> ReviewWithUserResponseList:
        key = await self.cache_key_service.build_list_key(
            entity=CacheEntity.review,
            action="get",
            size=size,
            page=page,
        )
        cached_reviews_response = await self.cache_service.get(
            key,
            ReviewWithUserResponseList,
        )
        if cached_reviews_response is not None:
            return cast(ReviewWithUserResponseList, cached_reviews_response)

        reviews_response = await self.review_service.get_reviews(size, page)
        await self.cache_service.set(
            key,
            reviews_response,
            ttl=30 * 60,
        )
        return reviews_response

    async def get_review_by_id(self, review_id: int) -> ReviewWithUserResponse:
        key = self.cache_key_service.build_item_key(
            entity=CacheEntity.review,
            entity_id=review_id,
            action="get",
        )
        cached_review_response = await self.cache_service.get(
            key,
            ReviewWithUserResponse,
        )
        if cached_review_response is not None:
            return cast(ReviewWithUserResponse, cached_review_response)

        review_response = await self.review_service.get_review_by_id(review_id)
        await self.cache_service.set(
            key,
            review_response,
            ttl=30 * 60,
        )
        return review_response

    async def get_user_reviews(
        self,
        user_id: int,
        size: int = 10,
        page: int = 1,
    ) -> ReviewWithMovieResponseList:
        key = await self.cache_key_service.build_list_key(
            entity=CacheEntity.review,
            action="get",
            user_id=user_id,
            size=size,
            page=page,
        )
        cached_reviews_response = await self.cache_service.get(
            key,
            ReviewWithMovieResponseList,
        )
        if cached_reviews_response is not None:
            return cast(ReviewWithMovieResponseList, cached_reviews_response)

        reviews_response = await self.review_service.get_user_reviews(
            user_id,
            size,
            page,
        )
        await self.cache_service.set(
            key,
            reviews_response,
            ttl=30 * 60,
        )
        return reviews_response

    async def get_user_review_about_movie(
        self,
        user_id: int,
        movie_id: int,
    ) -> ReviewResponse:
        entity_id = (user_id, movie_id)
        key = self.cache_key_service.build_item_key(
            entity=CacheEntity.review,
            entity_id=entity_id,
            action="get",
        )
        cached_review_response = await self.cache_service.get(key, ReviewResponse)
        if cached_review_response is not None:
            return cast(ReviewResponse, cached_review_response)

        review_response = await self.review_service.get_user_review_about_movie(
            user_id,
            movie_id,
        )
        await self.cache_service.set(
            key,
            review_response,
            ttl=30 * 60,
        )
        return review_response

    async def get_movie_reviews(
        self,
        movie_id: int,
        size: int = 10,
        page: int = 1,
    ) -> ReviewWithUserResponseList:
        key = await self.cache_key_service.build_list_key(
            entity=CacheEntity.review,
            action="get",
            movie_id=movie_id,
            size=size,
            page=page,
        )
        cached_reviews_response = await self.cache_service.get(
            key,
            ReviewWithUserResponseList,
        )
        if cached_reviews_response is not None:
            return cast(ReviewWithUserResponseList, cached_reviews_response)

        reviews_response = await self.review_service.get_movie_reviews(
            movie_id,
            size,
            page,
        )
        await self.cache_service.set(
            key,
            reviews_response,
            ttl=30 * 60,
        )
        return reviews_response

    async def get_low_rated_movie_reviews(
        self,
        movie_id: int,
        size: int,
        page: int,
    ) -> ReviewWithUserResponseList:
        key = await self.cache_key_service.build_list_key(
            entity=CacheEntity.review,
            action="get-low-rated",
            movie_id=movie_id,
            size=size,
            page=page,
        )
        cached_reviews_response = await self.cache_service.get(
            key,
            ReviewWithUserResponseList,
        )
        if cached_reviews_response is not None:
            return cast(ReviewWithUserResponseList, cached_reviews_response)

        reviews_response = await self.review_service.get_low_rated_movie_reviews(
            movie_id,
            size,
            page,
        )
        await self.cache_service.set(
            key,
            reviews_response,
            ttl=30 * 60,
        )
        return reviews_response

    async def get_top_rated_movie_reviews(
        self,
        movie_id: int,
        size: PaginationSizeDep = 10,
        page: PaginationPageDep = 1,
    ) -> ReviewWithUserResponseList:
        key = await self.cache_key_service.build_list_key(
            entity=CacheEntity.review,
            action="get-top-rated",
            movie_id=movie_id,
            size=size,
            page=page,
        )
        cached_reviews_response = await self.cache_service.get(
            key,
            ReviewWithUserResponseList,
        )
        if cached_reviews_response is not None:
            return cast(ReviewWithUserResponseList, cached_reviews_response)

        reviews_response = await self.review_service.get_top_rated_movie_reviews(
            movie_id,
            size,
            page,
        )
        await self.cache_service.set(
            key,
            reviews_response,
            ttl=1800,
        )
        return reviews_response

    async def get_top_newest_movie_reviews(
        self,
        movie_id: int,
        size: int,
        page: int,
    ) -> ReviewWithUserResponseList:
        key = await self.cache_key_service.build_list_key(
            entity=CacheEntity.review,
            action="get-top-newest",
            movie_id=movie_id,
            size=size,
            page=page,
        )
        cached_reviews_response = await self.cache_service.get(
            key,
            ReviewWithUserResponseList,
        )
        if cached_reviews_response is not None:
            return cast(ReviewWithUserResponseList, cached_reviews_response)

        reviews_response = await self.review_service.get_top_newest_movie_reviews(
            movie_id,
            size,
            page,
        )
        await self.cache_service.set(
            key,
            reviews_response,
            ttl=30 * 60,
        )
        return reviews_response

    async def get_top_oldest_movie_reviews(
        self,
        movie_id: int,
        size: int,
        page: int,
    ) -> ReviewWithUserResponseList:
        key = await self.cache_key_service.build_list_key(
            entity=CacheEntity.review,
            action="get-top-oldest",
            movie_id=movie_id,
            size=size,
            page=page,
        )
        cached_reviews_response = cast(
            ReviewWithUserResponseList,
            await self.cache_service.get(key, ReviewWithUserResponseList),
        )
        if cached_reviews_response is not None:
            return cached_reviews_response

        reviews_response = await self.review_service.get_top_oldest_movie_reviews(
            movie_id,
            size,
            page,
        )
        await self.cache_service.set(
            key,
            reviews_response,
            ttl=30 * 60,
        )
        return reviews_response

    async def create_review(
        self,
        user_id: int,
        create_review_data: ReviewCreate,
    ) -> ReviewWithUserResponse:
        review_response = await self.review_service.create_review(
            user_id,
            create_review_data,
        )
        pattern = await self.cache_key_service.build_list_regex_key(
            entity=CacheEntity.review,
            action_regex="get*",
            size="*",
            page="*",
        )
        await self.cache_service.delete_by_pattern(pattern)
        return review_response

    async def update_review(
        self,
        current_user_id: int,
        review_id: int,
        update_review_data: ReviewUpdate,
    ) -> ReviewWithUserResponse:
        review_response = await self.review_service.update_review(
            current_user_id,
            review_id,
            update_review_data,
        )
        pattern = await self.cache_key_service.build_list_regex_key(
            entity=CacheEntity.review,
            action_regex="get*",
            size="*",
            page="*",
        )
        key = self.cache_key_service.build_item_key(
            entity=CacheEntity.review,
            entity_id=review_id,
            action="get",
        )
        await asyncio.gather(
            self.cache_service.delete_by_pattern(pattern),
            self.cache_service.delete(key),
        )
        return review_response

    async def partial_update_review(
        self,
        current_user_id: int,
        review_id: int,
        update_review_data: ReviewPartialUpdate,
    ) -> ReviewWithUserResponse:
        review_response = await self.review_service.partial_update_review(
            current_user_id,
            review_id,
            update_review_data,
        )
        pattern = await self.cache_key_service.build_list_regex_key(
            entity=CacheEntity.review,
            action_regex="get*",
            size="*",
            page="*",
        )
        key = self.cache_key_service.build_item_key(
            entity=CacheEntity.review,
            entity_id=review_id,
            action="get",
        )
        await asyncio.gather(
            self.cache_service.delete_by_pattern(pattern),
            self.cache_service.delete(key),
        )
        return review_response

    async def delete_review(
        self,
        current_user_id: int,
        review_id: int,
    ) -> None:
        review = await self.review_service.delete_review(
            current_user_id,
            review_id,
        )
        pattern = await self.cache_key_service.build_list_regex_key(
            entity=CacheEntity.review,
            action_regex="get*",
            size="*",
            page="*",
        )
        user_id, movie_id = review.user_id, review.movie_id
        entity_id = (user_id, movie_id)
        key = self.cache_key_service.build_item_key(
            entity=CacheEntity.review,
            entity_id=entity_id,
            action="get",
        )
        await asyncio.gather(
            self.cache_service.delete_by_pattern(pattern),
            self.cache_service.delete(key),
        )
