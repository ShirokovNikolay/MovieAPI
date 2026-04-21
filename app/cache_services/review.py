from typing import cast

from core.redis.cache_service import CacheService
from dependencies.annotations.validators import PaginationPageDep, PaginationSizeDep
from schemas.review import (
    ReviewCreate,
    ReviewPartialUpdate,
    ReviewResponse,
    ReviewResponseList,
    ReviewUpdate,
)
from services import ReviewService


class ReviewCacheService:
    def __init__(
        self,
        review_service: ReviewService,
        cache_service: CacheService,
    ) -> None:
        self.review_service = review_service
        self.cache_service = cache_service

    async def get_reviews(
        self,
        size: int = 10,
        page: int = 1,
    ) -> ReviewResponseList:
        key = CacheService.create_cache_key("reviews", size=size, page=page)
        cached_reviews_response = await self.cache_service.get(key, ReviewResponseList)
        if cached_reviews_response is not None:
            return cast(ReviewResponseList, cached_reviews_response)

        reviews_response = await self.review_service.get_reviews(size, page)
        await self.cache_service.set(
            key,
            reviews_response,
            ttl=1800,
        )
        return reviews_response

    async def get_review_by_id(self, review_id: int) -> ReviewResponse:
        key = CacheService.create_cache_key("review", review_id=review_id)
        cached_review_response = await self.cache_service.get(key, ReviewResponse)
        if cached_review_response is not None:
            return cast(ReviewResponse, cached_review_response)

        review_response = await self.review_service.get_review_by_id(review_id)
        await self.cache_service.set(
            key,
            review_response,
            ttl=1800,
        )
        return review_response

    async def get_user_reviews(
        self,
        user_id: int,
        size: int = 10,
        page: int = 1,
    ) -> ReviewResponseList:
        key = CacheService.create_cache_key(
            "reviews",
            user_id=user_id,
            size=size,
            page=page,
        )
        cached_reviews_response = await self.cache_service.get(key, ReviewResponseList)
        if cached_reviews_response is not None:
            return cast(ReviewResponseList, cached_reviews_response)

        reviews_response = await self.review_service.get_user_reviews(
            user_id,
            size,
            page,
        )
        await self.cache_service.set(
            key,
            reviews_response,
            ttl=1800,
        )
        return reviews_response

    async def get_user_review_about_movie(
        self,
        user_id: int,
        movie_id: int,
    ) -> ReviewResponse:
        key = CacheService.create_cache_key(
            "review",
            user_id=user_id,
            movie_id=movie_id,
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
            ttl=1800,
        )
        return review_response

    async def get_movie_reviews(
        self,
        movie_id: int,
        size: int = 10,
        page: int = 1,
    ) -> ReviewResponseList:
        key = CacheService.create_cache_key(
            "reviews",
            movie_id=movie_id,
            size=size,
            page=page,
        )
        cached_reviews_response = await self.cache_service.get(key, ReviewResponseList)
        if cached_reviews_response is not None:
            return cast(ReviewResponseList, cached_reviews_response)

        reviews_response = await self.review_service.get_movie_reviews(
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

    async def get_top_rating_movie_reviews(
        self,
        movie_id: int,
        size: PaginationSizeDep = 10,
        page: PaginationPageDep = 1,
    ) -> ReviewResponseList:
        key = CacheService.create_cache_key(
            "reviews",
            movie_id=movie_id,
            size=size,
            page=page,
        )
        cached_reviews_response = await self.cache_service.get(key, ReviewResponseList)
        if cached_reviews_response is not None:
            return cast(ReviewResponseList, cached_reviews_response)

        reviews_response = await self.review_service.get_top_rating_movie_reviews(
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
    ) -> ReviewResponseList:
        key = CacheService.create_cache_key(
            "reviews",
            movie_id=movie_id,
            size=size,
            page=page,
        )
        cached_reviews_response = await self.cache_service.get(key, ReviewResponseList)
        if cached_reviews_response is not None:
            return cast(ReviewResponseList, cached_reviews_response)

        reviews_response = await self.review_service.get_top_newest_movie_reviews(
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

    async def get_top_oldest_movie_reviews(
        self,
        movie_id: int,
        size: int,
        page: int,
    ) -> ReviewResponseList:
        key = CacheService.create_cache_key(
            "reviews",
            movie_id=movie_id,
            size=size,
            page=page,
        )
        cached_reviews_response = cast(
            ReviewResponseList,
            await self.cache_service.get(key, ReviewResponseList),
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
            ttl=1800,
        )
        return reviews_response

    async def create_review(
        self,
        user_id: int,
        create_review_data: ReviewCreate,
    ) -> ReviewResponse:
        review_response = await self.review_service.create_review(
            user_id,
            create_review_data,
        )
        key = CacheService.create_cache_key("review")
        pattern = key + "*"
        await self.cache_service.delete_by_pattern(pattern)
        return review_response

    async def update_review(
        self,
        current_user_id: int,
        review_id: int,
        update_review_data: ReviewUpdate,
    ) -> ReviewResponse:
        review_response = await self.review_service.update_review(
            current_user_id,
            review_id,
            update_review_data,
        )
        key = CacheService.create_cache_key("review")
        pattern = key + "*"
        await self.cache_service.delete_by_pattern(pattern)
        return review_response

    async def partial_update_review(
        self,
        current_user_id: int,
        review_id: int,
        update_review_data: ReviewPartialUpdate,
    ) -> ReviewResponse:
        review_response = await self.review_service.partial_update_review(
            current_user_id,
            review_id,
            update_review_data,
        )
        key = CacheService.create_cache_key("review")
        pattern = key + "*"
        await self.cache_service.delete_by_pattern(pattern)
        return review_response

    async def delete_review(
        self,
        current_user_id: int,
        review_id: int,
    ) -> None:
        await self.review_service.delete_review(
            current_user_id,
            review_id,
        )
        key = CacheService.create_cache_key("review")
        pattern = key + "*"
        await self.cache_service.delete_by_pattern(pattern)
