from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import UserRole
from core.exceptions.auth import PermissionDeniedError
from core.exceptions.movie import MovieIdNotFoundError
from core.exceptions.review import (
    ReviewAlreadyExistsByUserAndMovieError,
    ReviewIdNotFoundError,
    ReviewNotFoundByUserAndMovieError,
)
from core.exceptions.user import UserIdNotFoundError
from repositories import MovieRepository, ReviewRepository, UserRepository
from schemas.review import (
    ReviewCreate,
    ReviewPartialUpdate,
    ReviewResponse,
    ReviewUpdate,
    ReviewWithMovieResponse,
    ReviewWithMovieResponseList,
    ReviewWithUserResponse,
    ReviewWithUserResponseList,
)
from schemas.user import UserResponse


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
    ) -> ReviewWithUserResponseList:
        reviews = [
            ReviewWithUserResponse.model_validate(movie)
            for movie in await self.review_repository.get_all_reviews(size, page)
        ]
        return ReviewWithUserResponseList(
            review_list=reviews,
            size=size,
            page=page,
        )

    async def get_review_by_id(self, review_id: int) -> ReviewWithUserResponse:
        review = await self.review_repository.get_review_by_id(review_id)
        if review is not None:
            return ReviewWithUserResponse.model_validate(review)
        raise ReviewIdNotFoundError(review_id)

    async def get_user_reviews(
        self,
        user_id: int,
        size: int = 10,
        page: int = 1,
    ) -> ReviewWithMovieResponseList:
        if not await self.user_repository.user_id_exists(user_id):
            raise UserIdNotFoundError(user_id)

        reviews = [
            ReviewWithMovieResponse.model_validate(review)
            for review in await self.review_repository.get_user_reviews(
                user_id,
                size,
                page,
            )
        ]
        return ReviewWithMovieResponseList(
            review_list=reviews,
            size=size,
            page=page,
        )

    async def get_user_review_about_movie(
        self,
        user_id: int,
        movie_id: int,
    ) -> ReviewResponse:
        if not await self.user_repository.user_id_exists(user_id):
            raise UserIdNotFoundError(user_id)

        if not await self.movie_repository.movie_id_exists(movie_id):
            raise MovieIdNotFoundError(movie_id)

        review = await self.review_repository.get_user_review_about_movie(
            user_id,
            movie_id,
        )
        if review is None:
            raise ReviewNotFoundByUserAndMovieError(user_id, movie_id)

        return ReviewResponse.model_validate(review)

    async def get_movie_reviews(
        self,
        movie_id: int,
        size: int = 10,
        page: int = 1,
    ) -> ReviewWithUserResponseList:
        if not await self.movie_repository.movie_id_exists(movie_id):
            raise MovieIdNotFoundError(movie_id)

        reviews = [
            ReviewWithUserResponse.model_validate(review)
            for review in await self.review_repository.get_movie_reviews(
                movie_id,
                size,
                page,
            )
        ]
        return ReviewWithUserResponseList(
            review_list=reviews,
            size=size,
            page=page,
        )

    async def get_low_rated_movie_reviews(
        self,
        movie_id: int,
        size: int,
        page: int,
    ) -> ReviewWithUserResponseList:
        if not await self.movie_repository.movie_id_exists(movie_id):
            raise MovieIdNotFoundError(movie_id)
        reviews = [
            ReviewWithUserResponse.model_validate(review)
            for review in await self.review_repository.get_low_rated_movie_reviews(
                movie_id,
                size,
                page,
            )
        ]
        return ReviewWithUserResponseList(
            review_list=reviews,
            page=page,
            size=size,
        )

    async def get_top_rated_movie_reviews(
        self,
        movie_id: int,
        size: int,
        page: int,
    ) -> ReviewWithUserResponseList:
        if not await self.movie_repository.movie_id_exists(movie_id):
            raise MovieIdNotFoundError(movie_id)

        reviews = [
            ReviewWithUserResponse.model_validate(review)
            for review in await self.review_repository.get_top_rated_movie_reviews(
                movie_id,
                size,
                page,
            )
        ]
        return ReviewWithUserResponseList(
            review_list=reviews,
            size=size,
            page=page,
        )

    async def get_top_newest_movie_reviews(
        self,
        movie_id: int,
        size: int,
        page: int,
    ) -> ReviewWithUserResponseList:
        if not await self.movie_repository.movie_id_exists(movie_id):
            raise MovieIdNotFoundError(movie_id)

        reviews = [
            ReviewWithUserResponse.model_validate(review)
            for review in await self.review_repository.get_top_newest_movie_reviews(
                movie_id,
                size,
                page,
            )
        ]
        return ReviewWithUserResponseList(
            review_list=reviews,
            size=size,
            page=page,
        )

    async def get_top_oldest_movie_reviews(
        self,
        movie_id: int,
        size: int,
        page: int,
    ) -> ReviewWithUserResponseList:
        if not await self.movie_repository.movie_id_exists(movie_id):
            raise MovieIdNotFoundError(movie_id)

        reviews = [
            ReviewWithUserResponse.model_validate(review)
            for review in await self.review_repository.get_top_oldest_movie_reviews(
                movie_id,
                size,
                page,
            )
        ]
        return ReviewWithUserResponseList(
            review_list=reviews,
            size=size,
            page=page,
        )

    async def create_review(
        self,
        user_id: int,
        create_review_data: ReviewCreate,
    ) -> ReviewWithUserResponse:
        if not await self.user_repository.user_id_exists(user_id):
            raise UserIdNotFoundError(user_id)

        if not await self.movie_repository.movie_id_exists(create_review_data.movie_id):
            raise MovieIdNotFoundError(create_review_data.movie_id)

        if await self.review_repository.review_exists(
            create_review_data.movie_id,
            user_id,
        ):
            raise ReviewAlreadyExistsByUserAndMovieError(
                create_review_data.movie_id,
                user_id,
            )

        review = await self.review_repository.create_review(user_id, create_review_data)
        return ReviewWithUserResponse.model_validate(review)

    async def update_review(
        self,
        current_user_id: int,
        review_id: int,
        update_review_data: ReviewUpdate,
    ) -> ReviewWithUserResponse:
        if not await self.user_repository.user_id_exists(current_user_id):
            raise UserIdNotFoundError(current_user_id)

        review_owner = await self.get_review_owner(review_id)
        if review_owner.id != current_user_id:
            raise PermissionDeniedError

        updated_review = await self.review_repository.update_review(
            review_id,
            update_review_data,
        )
        return ReviewWithUserResponse.model_validate(updated_review)

    async def partial_update_review(
        self,
        current_user_id: int,
        review_id: int,
        update_review_data: ReviewPartialUpdate,
    ) -> ReviewWithUserResponse:
        if not await self.user_repository.user_id_exists(current_user_id):
            raise UserIdNotFoundError(current_user_id)

        review_owner = await self.get_review_owner(review_id)
        if review_owner.id != current_user_id:
            raise PermissionDeniedError

        updated_review = await self.review_repository.partial_update_review(
            review_id,
            update_review_data,
        )
        return ReviewWithUserResponse.model_validate(updated_review)

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
            raise PermissionDeniedError

        await self.review_repository.delete_review(review_id)

    async def get_review_owner(self, review_id: int) -> UserResponse:
        user = await self.review_repository.get_review_owner(review_id)
        if user is not None:
            return UserResponse.model_validate(user)

        raise ReviewIdNotFoundError(review_id)
