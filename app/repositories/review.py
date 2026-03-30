from sqlalchemy import and_, desc

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from models import Review, User
from schemas.review import ReviewCreate, ReviewPartialUpdate, ReviewUpdate


class ReviewRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_review_owner(self, review_id: int) -> User | None:
        stmt = (
            select(User)
            .join(Review, Review.user_id == User.id)
            .where(Review.id == review_id)
        )
        return self.session.execute(stmt).scalars().first()

    def get_all_reviews(self) -> list[Review]:
        stmt = select(Review)
        return list(self.session.execute(stmt).scalars().all())

    def get_review_by_id(self, review_id: int) -> Review | None:
        stmt = select(Review).where(Review.id == review_id)
        return self.session.execute(stmt).scalars().first()

    def get_review_by_user_id_and_movie_id(
        self, user_id: int, movie_id: int
    ) -> Review | None:
        stmt = select(Review).where(
            and_(Review.user_id == user_id, Review.movie_id == movie_id)
        )
        return self.session.execute(stmt).scalars().first()

    def review_exists(self, movie_id: int, user_id: int) -> bool:
        return self.get_review_by_user_id_and_movie_id(user_id, movie_id) is not None

    def review_id_exists(self, review_id: int) -> bool:
        return self.get_review_by_id(review_id) is not None

    def get_user_reviews(self, user_id: int) -> list[Review]:
        stmt = (
            select(Review)
            .options(
                joinedload(Review.user),
            )
            .where(
                Review.user_id == user_id,
            )
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_user_review_about_movie(self, user_id: int, movie_id: int) -> Review | None:
        stmt = (
            select(Review)
            .options(
                joinedload(Review.user),
                joinedload(Review.movie),
            )
            .where(
                and_(
                    Review.user_id == user_id,
                    Review.movie_id == movie_id,
                )
            )
        )
        return self.session.execute(stmt).scalars().first()

    def get_movie_reviews(self, movie_id: int) -> list[Review]:
        stmt = (
            select(Review)
            .options(
                selectinload(Review.user),
                joinedload(Review.movie),
            )
            .where(
                Review.movie_id == movie_id,
            )
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_top_rating_movie_reviews(
        self,
        movie_id: int,
        limit: int,
    ) -> list[Review]:
        stmt = (
            select(Review)
            .options(
                joinedload(Review.movie),
                joinedload(Review.user),
            )
            .where(Review.movie_id == movie_id)
            .order_by(desc(Review.rating))
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_top_newest_movie_reviews(self, movie_id: int, limit: int) -> list[Review]:
        stmt = (
            select(Review)
            .options(
                joinedload(Review.movie),
                joinedload(Review.user),
            )
            .where(Review.movie_id == movie_id)
            .order_by(desc(Review.publication_date))
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_top_oldest_movie_reviews(self, movie_id: int, limit: int) -> list[Review]:
        stmt = (
            select(Review)
            .options(
                joinedload(Review.movie),
                joinedload(Review.user),
            )
            .where(Review.movie_id == movie_id)
            .order_by(Review.publication_date)
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars().all())

    def create_review(
        self,
        user_id: int,
        create_review_data: ReviewCreate,
    ) -> Review:
        review = Review(user_id=user_id, **create_review_data.model_dump())
        self.session.add(review)
        self.session.commit()
        self.session.refresh(review)
        return review

    def update_review(
        self,
        review_id: int,
        update_review_data: ReviewUpdate,
    ) -> Review | None:
        review = self.get_review_by_id(review_id)
        if review is None:
            return None

        for field, value in update_review_data.model_dump().items():
            setattr(review, field, value)

        self.session.commit()
        self.session.refresh(review)
        return review

    def partial_update_review(
        self,
        review_id: int,
        update_review_data: ReviewPartialUpdate,
    ) -> Review | None:
        review = self.get_review_by_id(review_id)
        if review is None:
            return None

        for field, value in update_review_data.model_dump(exclude_unset=True).items():
            setattr(review, field, value)

        self.session.commit()
        self.session.refresh(review)
        return review

    def delete_review(self, review_id: int) -> bool:
        if self.get_review_by_id(review_id) is None:
            return False

        stmt = delete(Review).where(Review.id == review_id)
        self.session.execute(stmt)
        self.session.commit()
        return True
