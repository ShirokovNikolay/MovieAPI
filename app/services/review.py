from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import UserRole
from repositories import ReviewRepository, UserRepository, MovieRepository
from fastapi import status
from schemas.review import (
    ReviewResponse,
    ReviewResponseList,
    ReviewCreate,
    ReviewUpdate,
    ReviewPartialUpdate,
)
from schemas.user import UserResponse


class ReviewService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repository = UserRepository(session)
        self.movie_repository = MovieRepository(session)
        self.review_repository = ReviewRepository(session)

    async def get_reviews(self) -> ReviewResponseList:
        reviews = [
            ReviewResponse.model_validate(movie)
            for movie in await self.review_repository.get_all_reviews()
        ]
        return ReviewResponseList(review_list=reviews)

    async def get_review_by_id(self, review_id: int) -> ReviewResponse:
        review = await self.review_repository.get_review_by_id(review_id)
        if review is not None:
            return ReviewResponse.model_validate(review)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with {review_id=} not found",
        )

    async def get_user_reviews(self, user_id: int) -> ReviewResponseList:
        if not await self.user_repository.user_id_exists(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with {user_id=} not found",
            )
        reviews = [
            ReviewResponse.model_validate(review)
            for review in await self.review_repository.get_user_reviews(user_id)
        ]
        return ReviewResponseList(review_list=reviews)

    async def get_user_review_about_movie(
        self, user_id: int, movie_id: int
    ) -> ReviewResponse:
        if not await self.user_repository.user_id_exists(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with {user_id=} not found",
            )

        if not await self.movie_repository.movie_id_exists(movie_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with {movie_id=} not found",
            )

        review = await self.review_repository.get_user_review_about_movie(
            user_id, movie_id
        )
        if review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Review with {user_id=} and {movie_id=} not found",
            )

        return ReviewResponse.model_validate(review)

    async def get_movie_reviews(self, movie_id: int) -> ReviewResponseList:
        if not await self.movie_repository.movie_id_exists(movie_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with {movie_id=} not found",
            )

        reviews = [
            ReviewResponse.model_validate(review)
            for review in await self.review_repository.get_movie_reviews(movie_id)
        ]
        return ReviewResponseList(review_list=reviews)

    async def get_top_rating_movie_reviews(
        self,
        movie_id: int,
        limit: int,
    ) -> ReviewResponseList:
        if not await self.movie_repository.movie_id_exists(movie_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with {movie_id=} not found",
            )
        reviews = [
            ReviewResponse.model_validate(review)
            for review in await self.review_repository.get_top_rating_movie_reviews(
                movie_id, limit
            )
        ]
        return ReviewResponseList(review_list=reviews)

    async def get_top_newest_movie_reviews(
        self,
        movie_id: int,
        limit: int,
    ) -> ReviewResponseList:
        if not await self.movie_repository.movie_id_exists(movie_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with {movie_id=} not found",
            )
        reviews = [
            ReviewResponse.model_validate(review)
            for review in await self.review_repository.get_top_newest_movie_reviews(
                movie_id, limit
            )
        ]
        return ReviewResponseList(review_list=reviews)

    async def get_top_oldest_movie_reviews(
        self,
        movie_id: int,
        limit: int,
    ) -> ReviewResponseList:
        if not await self.movie_repository.movie_id_exists(movie_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with {movie_id=} not found",
            )
        reviews = [
            ReviewResponse.model_validate(review)
            for review in await self.review_repository.get_top_oldest_movie_reviews(
                movie_id, limit
            )
        ]
        return ReviewResponseList(review_list=reviews)

    async def create_review(
        self,
        user_id: int,
        create_review_data: ReviewCreate,
    ) -> ReviewResponse:
        if not await self.user_repository.user_id_exists(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with {user_id=} not found",
            )
        if not await self.movie_repository.movie_id_exists(create_review_data.movie_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with movie_id={create_review_data.movie_id} not found",
            )

        if await self.review_repository.review_exists(
            create_review_data.movie_id, user_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Review with {user_id=} and movie_id={create_review_data.movie_id} already exists",
            )

        review = await self.review_repository.create_review(user_id, create_review_data)
        return ReviewResponse.model_validate(review)

    async def update_review(
        self,
        current_user_id: int,
        review_id: int,
        update_review_data: ReviewUpdate,
    ) -> ReviewResponse:
        if not await self.user_repository.user_id_exists(current_user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with {current_user_id=} not found",
            )

        review_owner = await self.get_review_owner(review_id)
        if review_owner.id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User with user_id={current_user_id} is not allowed to update review with review_id={review_id}",
            )

        updated_review = await self.review_repository.update_review(
            review_id, update_review_data
        )
        return ReviewResponse.model_validate(updated_review)

    async def partial_update_review(
        self,
        current_user_id: int,
        review_id: int,
        update_review_data: ReviewPartialUpdate,
    ) -> ReviewResponse:
        if not await self.user_repository.user_id_exists(current_user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with {current_user_id=} not found",
            )

        review_owner = await self.get_review_owner(review_id)
        if review_owner.id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User with user_id={current_user_id} is not allowed to update review with review_id={review_id}",
            )

        updated_review = await self.review_repository.partial_update_review(
            review_id, update_review_data
        )
        return ReviewResponse.model_validate(updated_review)

    async def delete_review(
        self,
        current_user_id: int,
        review_id: int,
    ) -> None:
        if not await self.user_repository.user_id_exists(current_user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with {current_user_id=} not found",
            )

        review_owner = await self.get_review_owner(review_id)

        if (
            review_owner.id != current_user_id
            and await self.user_repository.get_user_role(current_user_id)
            != UserRole.admin.value
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You are not allowed to delete review with review_id={review_id}",
            )

        await self.review_repository.delete_review(review_id)

    async def get_review_owner(self, review_id: int) -> UserResponse:
        user = await self.review_repository.get_review_owner(review_id)
        if user is not None:
            return UserResponse.model_validate(user)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with {review_id=} not found",
        )
