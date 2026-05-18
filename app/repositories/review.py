from sqlalchemy import and_, delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import Review, User
from schemas.review import ReviewCreate, ReviewPartialUpdate, ReviewUpdate


class ReviewRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_review_owner(self, review_id: int) -> User | None:
        stmt = (
            select(User)
            .join(Review, Review.user_id == User.id)
            .where(Review.id == review_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_reviews(
        self,
        size: int = 10,
        page: int = 1,
    ) -> list[Review]:
        stmt = (
            select(Review)
            .options(joinedload(Review.user))
            .limit(size)
            .offset(size * (page - 1))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_review_by_id(self, review_id: int) -> Review | None:
        stmt = (
            select(Review)
            .options(joinedload(Review.user))
            .where(Review.id == review_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def review_exists(self, movie_id: int, user_id: int) -> bool:
        return await self.get_user_review_about_movie(user_id, movie_id) is not None

    async def review_id_exists(self, review_id: int) -> bool:
        return await self.get_review_by_id(review_id) is not None

    async def get_user_reviews(
        self,
        user_id: int,
        size: int = 10,
        page: int = 1,
    ) -> list[Review]:
        stmt = (
            select(Review)
            .where(
                Review.user_id == user_id,
            )
            .limit(size)
            .offset(size * (page - 1))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_user_review_about_movie(
        self,
        user_id: int,
        movie_id: int,
    ) -> Review | None:
        stmt = select(Review).where(
            and_(
                Review.user_id == user_id,
                Review.movie_id == movie_id,
            ),
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_movie_reviews(
        self,
        movie_id: int,
        size: int = 10,
        page: int = 1,
    ) -> list[Review]:
        stmt = (
            select(Review)
            .options(joinedload(Review.user))
            .where(
                Review.movie_id == movie_id,
            )
            .limit(size)
            .offset(size * (page - 1))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_low_rated_movie_reviews(
        self,
        movie_id: int,
        size: int,
        page: int,
    ) -> list[Review]:
        stmt = (
            select(Review)
            .options(joinedload(Review.user))
            .where(Review.movie_id == movie_id)
            .order_by(Review.rating)
            .limit(size)
            .offset(size * (page - 1))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_top_rated_movie_reviews(
        self,
        movie_id: int,
        size: int,
        page: int,
    ) -> list[Review]:
        stmt = (
            select(Review)
            .options(joinedload(Review.user))
            .where(Review.movie_id == movie_id)
            .order_by(desc(Review.rating))
            .limit(size)
            .offset(size * (page - 1))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_top_newest_movie_reviews(
        self,
        movie_id: int,
        size: int,
        page: int,
    ) -> list[Review]:
        stmt = (
            select(Review)
            .options(joinedload(Review.user))
            .where(Review.movie_id == movie_id)
            .order_by(desc(Review.publication_date))
            .limit(size)
            .offset(size * (page - 1))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_top_oldest_movie_reviews(
        self,
        movie_id: int,
        size: int,
        page: int,
    ) -> list[Review]:
        stmt = (
            select(Review)
            .options(joinedload(Review.user))
            .where(Review.movie_id == movie_id)
            .order_by(Review.publication_date)
            .limit(size)
            .offset(size * (page - 1))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_review(
        self,
        user_id: int,
        create_review_data: ReviewCreate,
    ) -> Review | None:
        review = Review(user_id=user_id, **create_review_data.model_dump())
        self.session.add(review)
        await self.session.commit()
        await self.session.refresh(review)
        return await self.get_review_by_id(review.id)

    async def update_review(
        self,
        review_id: int,
        update_review_data: ReviewUpdate,
    ) -> Review | None:
        review = await self.get_review_by_id(review_id)
        if review is None:
            return None

        for field, value in update_review_data.model_dump().items():
            setattr(review, field, value)

        await self.session.commit()
        await self.session.refresh(review)
        return await self.get_review_by_id(review.id)

    async def partial_update_review(
        self,
        review_id: int,
        update_review_data: ReviewPartialUpdate,
    ) -> Review | None:
        review = await self.get_review_by_id(review_id)
        if review is None:
            return None

        for field, value in update_review_data.model_dump(exclude_unset=True).items():
            setattr(review, field, value)

        await self.session.commit()
        await self.session.refresh(review)
        return await self.get_review_by_id(review.id)

    async def delete_review(self, review_id: int) -> bool:
        if await self.get_review_by_id(review_id) is None:
            return False

        stmt = delete(Review).where(Review.id == review_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return True
