from fastapi import HTTPException

from repositories import ReviewRepository, UserRepository, MovieRepository
from sqlalchemy.orm import Session
from fastapi import status
from schemas.review import (
    ReviewResponse,
    ReviewResponseList,
    ReviewCreate,
    ReviewUpdate,
    ReviewPartialUpdate,
)

# details_review_views: prefix_router = /{review_id}
# 1) get_review_by_id
# 2) update_review
# 3) partial_update_review
# 4) delete_review


# details_user_views:   prefix_router = "/user"
# 1) get_user_reviews
# 2) get_user_review_about_movie

# details_movie_views:  prefix_router = "/movie"
# 1) get_movie_reviews
# 2) get_top_rating_movie_reviews
# 3) get_top_newest_movie_reviews
# 4) get_top_oldest_movie_reviews


# list_views:  prefix_router = ""
# 1) get_reviews
# 2) create_review


class ReviewService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.user_repository = UserRepository(session)
        self.movie_repository = MovieRepository(session)
        self.review_repository = ReviewRepository(session)

    def get_reviews(self) -> ReviewResponseList:
        reviews = [
            ReviewResponse.model_validate(movie)
            for movie in self.review_repository.get_all_reviews()
        ]
        return ReviewResponseList(review_list=reviews)

    def get_review_by_id(self, review_id: int) -> ReviewResponse:
        review = self.review_repository.get_review_by_id(review_id)
        if review is not None:
            return ReviewResponse.model_validate(review)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with {review_id=} not found",
        )

    def get_user_reviews(self, user_id: int) -> ReviewResponseList:
        if not self.user_repository.user_id_exists(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with {user_id=} not found",
            )
        reviews = [
            ReviewResponse.model_validate(review)
            for review in self.review_repository.get_user_reviews(user_id)
        ]
        return ReviewResponseList(review_list=reviews)

    def get_user_review_about_movie(
        self, user_id: int, movie_id: int
    ) -> ReviewResponse:
        if not self.user_repository.user_id_exists(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with {user_id=} not found",
            )

        if not self.movie_repository.movie_id_exists(movie_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with {movie_id=} not found",
            )

        review = self.review_repository.get_user_review_about_movie(user_id, movie_id)
        if review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Review with {user_id=} and {movie_id=} not found",
            )

        return ReviewResponse.model_validate(review)

    def get_movie_reviews(self, movie_id: int) -> ReviewResponseList:
        if not self.movie_repository.movie_id_exists(movie_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with {movie_id=} not found",
            )

        reviews = [
            ReviewResponse.model_validate(review)
            for review in self.review_repository.get_movie_reviews(movie_id)
        ]
        return ReviewResponseList(review_list=reviews)

    def get_top_rating_movie_reviews(
        self,
        movie_id: int,
        limit: int,
    ) -> ReviewResponseList:
        if not self.movie_repository.movie_id_exists(movie_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with {movie_id=} not found",
            )
        reviews = [
            ReviewResponse.model_validate(review)
            for review in self.review_repository.get_top_rating_movie_reviews(
                movie_id, limit
            )
        ]
        return ReviewResponseList(review_list=reviews)

    def get_top_newest_movie_reviews(
        self,
        movie_id: int,
        limit: int,
    ) -> ReviewResponseList:
        if not self.movie_repository.movie_id_exists(movie_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with {movie_id=} not found",
            )
        reviews = [
            ReviewResponse.model_validate(review)
            for review in self.review_repository.get_top_newest_movie_reviews(
                movie_id, limit
            )
        ]
        return ReviewResponseList(review_list=reviews)

    def get_top_oldest_movie_reviews(
        self,
        movie_id: int,
        limit: int,
    ) -> ReviewResponseList:
        if not self.movie_repository.movie_id_exists(movie_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with {movie_id=} not found",
            )
        reviews = [
            ReviewResponse.model_validate(review)
            for review in self.review_repository.get_top_oldest_movie_reviews(
                movie_id, limit
            )
        ]
        return ReviewResponseList(review_list=reviews)

    def create_review(
        self,
        user_id: int,
        create_review_data: ReviewCreate,
    ) -> ReviewResponse:
        if not self.user_repository.user_id_exists(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with {user_id=} not found",
            )
        if not self.movie_repository.movie_id_exists(create_review_data.movie_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with movie_id={create_review_data.movie_id} not found",
            )

        if self.review_repository.review_exists(create_review_data.movie_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Review with {user_id=} and movie_id={create_review_data.movie_id} already exists",
            )

        review = self.review_repository.create_review(user_id, create_review_data)
        return ReviewResponse.model_validate(review)

    def update_review(
        self,
        current_user_id: int,
        review_id: int,
        update_review_data: ReviewUpdate,
    ) -> ReviewResponse:
        if not self.user_repository.user_id_exists(current_user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with {current_user_id=} not found",
            )

        review = self.review_repository.get_review_by_id(review_id)
        if review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Review with {review_id=} not found",
            )

        if review.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User with user_id={current_user_id} is not allowed to update review with review_id={review.id}",
            )

        updated_review = self.review_repository.update_review(
            review_id, update_review_data
        )
        return ReviewResponse.model_validate(updated_review)

    def partial_update_review(
        self,
        current_user_id: int,
        review_id: int,
        update_review_data: ReviewPartialUpdate,
    ) -> ReviewResponse:
        if not self.user_repository.user_id_exists(current_user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with {current_user_id=} not found",
            )

        review = self.review_repository.get_review_by_id(review_id)
        if review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Review with {review_id=} not found",
            )

        if review.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User with user_id={current_user_id} is not allowed to update review with review_id={review.id}",
            )

        updated_review = self.review_repository.partial_update_review(
            review_id, update_review_data
        )
        return ReviewResponse.model_validate(updated_review)

    def delete_review(
        self,
        current_user_id: int,
        review_id: int,
    ) -> None:
        if not self.user_repository.user_id_exists(current_user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with {current_user_id=} not found",
            )

        review = self.review_repository.get_review_by_id(review_id)
        if review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Review with {review_id=} not found",
            )

        if review.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User with user_id={current_user_id} is not allowed to delete review with review_id={review.id}",
            )
        self.review_repository.delete_review(review_id)
