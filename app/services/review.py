from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import UserRole
from core.exceptions.user import UserIdNotFoundError
from repositories import ReviewRepository, UserRepository, MovieRepository
from schemas.review import (
    ReviewResponse,
    ReviewResponseList,
    ReviewCreate,
    ReviewUpdate,
    ReviewPartialUpdate,
)
from schemas.user import UserResponse

from core.exceptions.auth import PermissionDeniedError
from core.exceptions.movie import MovieIdNotFoundError
from core.exceptions.review import (
    ReviewIdNotFoundError,
    ReviewNotFoundByUserAndMovieError,
    ReviewAlreadyExistsByUserAndMovieError,
)


class ReviewService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repository = UserRepository(session)
        self.movie_repository = MovieRepository(session)
        self.review_repository = ReviewRepository(session)

    async def get_reviews(
        self,
        size: int = 10,
        page: int = 1,
    ) -> ReviewResponseList:
        reviews = [
            ReviewResponse.model_validate(movie)
            for movie in await self.review_repository.get_all_reviews(size, page)
        ]
        return ReviewResponseList(
            review_list=reviews,
            size=size,
            page=page,
        )

    async def get_review_by_id(self, review_id: int) -> ReviewResponse:
        review = await self.review_repository.get_review_by_id(review_id)
        if review is not None:
            return ReviewResponse.model_validate(review)
        raise ReviewIdNotFoundError(review_id)

    async def get_user_reviews(
        self,
        user_id: int,
        size: int = 10,
        page: int = 1,
    ) -> ReviewResponseList:
        if not await self.user_repository.user_id_exists(user_id):
            raise UserIdNotFoundError(user_id)

        reviews = [
            ReviewResponse.model_validate(review)
            for review in await self.review_repository.get_user_reviews(
                user_id,
                size,
                page,
            )
        ]
        return ReviewResponseList(
            review_list=reviews,
            size=size,
            page=page,
        )

    async def get_user_review_about_movie(
        self, user_id: int, movie_id: int
    ) -> ReviewResponse:
        if not await self.user_repository.user_id_exists(user_id):
            raise UserIdNotFoundError(user_id)

        if not await self.movie_repository.movie_id_exists(movie_id):
            raise MovieIdNotFoundError(movie_id)

        review = await self.review_repository.get_user_review_about_movie(
            user_id, movie_id
        )
        if review is None:
            raise ReviewNotFoundByUserAndMovieError(user_id, movie_id)

        return ReviewResponse.model_validate(review)

    async def get_movie_reviews(
        self,
        movie_id: int,
        size: int = 10,
        page: int = 1,
    ) -> ReviewResponseList:
        if not await self.movie_repository.movie_id_exists(movie_id):
            raise MovieIdNotFoundError(movie_id)

        reviews = [
            ReviewResponse.model_validate(review)
            for review in await self.review_repository.get_movie_reviews(
                movie_id,
                size,
                page,
            )
        ]
        return ReviewResponseList(
            review_list=reviews,
            size=size,
            page=page,
        )

    async def get_top_rating_movie_reviews(
        self,
        movie_id: int,
        limit: int,
    ) -> ReviewResponseList:
        if not await self.movie_repository.movie_id_exists(movie_id):
            raise MovieIdNotFoundError(movie_id)

        reviews = [
            ReviewResponse.model_validate(review)
            for review in await self.review_repository.get_top_rating_movie_reviews(
                movie_id, limit
            )
        ]
        return ReviewResponseList(review_list=reviews, size=limit)

    async def get_top_newest_movie_reviews(
        self,
        movie_id: int,
        limit: int,
    ) -> ReviewResponseList:
        if not await self.movie_repository.movie_id_exists(movie_id):
            raise MovieIdNotFoundError(movie_id)

        reviews = [
            ReviewResponse.model_validate(review)
            for review in await self.review_repository.get_top_newest_movie_reviews(
                movie_id, limit
            )
        ]
        return ReviewResponseList(review_list=reviews, size=limit)

    async def get_top_oldest_movie_reviews(
        self,
        movie_id: int,
        limit: int,
    ) -> ReviewResponseList:
        if not await self.movie_repository.movie_id_exists(movie_id):
            raise MovieIdNotFoundError(movie_id)

        reviews = [
            ReviewResponse.model_validate(review)
            for review in await self.review_repository.get_top_oldest_movie_reviews(
                movie_id, limit
            )
        ]
        return ReviewResponseList(review_list=reviews, size=limit)

    async def create_review(
        self,
        user_id: int,
        create_review_data: ReviewCreate,
    ) -> ReviewResponse:
        if not await self.user_repository.user_id_exists(user_id):
            raise UserIdNotFoundError(user_id)

        if not await self.movie_repository.movie_id_exists(create_review_data.movie_id):
            raise MovieIdNotFoundError(create_review_data.movie_id)

        if await self.review_repository.review_exists(
            create_review_data.movie_id, user_id
        ):
            raise ReviewAlreadyExistsByUserAndMovieError(
                create_review_data.movie_id, user_id
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
            raise UserIdNotFoundError(current_user_id)

        review_owner = await self.get_review_owner(review_id)
        if review_owner.id != current_user_id:
            raise PermissionDeniedError()

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
            raise UserIdNotFoundError(current_user_id)

        review_owner = await self.get_review_owner(review_id)
        if review_owner.id != current_user_id:
            raise PermissionDeniedError()

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
            raise UserIdNotFoundError(current_user_id)

        review_owner = await self.get_review_owner(review_id)

        if (
            review_owner.id != current_user_id
            and await self.user_repository.get_user_role(current_user_id)
            != UserRole.admin.value
        ):
            raise PermissionDeniedError()

        await self.review_repository.delete_review(review_id)

    async def get_review_owner(self, review_id: int) -> UserResponse:
        user = await self.review_repository.get_review_owner(review_id)
        if user is not None:
            return UserResponse.model_validate(user)

        raise ReviewIdNotFoundError(review_id)
