from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from models import Genre, User
from schemas.user import UserCreate, UserUpdate, UserPartialUpdate


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def user_id_exists(self, user_id: int) -> bool:
        return self.get_user_by_id(user_id) is not None

    def get_user_by_login(self, login: str) -> User | None:
        stmt = select(User).where(User.login == login)
        return self.session.execute(stmt).scalars().first()

    def get_all_users(self) -> list[User]:
        stmt = select(User)
        return list(self.session.execute(stmt).scalars().all())

    def create_user(self, create_user_data: UserCreate) -> User:
        user = User(**create_user_data.model_dump())
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update_user(
        self,
        user_id: int,
        update_data: UserUpdate,
    ) -> User | None:
        user = self.get_user_by_id(user_id)
        if user is None:
            return None

        for field, value in update_data.model_dump():
            setattr(user, field, value)

        self.session.commit()
        self.session.refresh(user)
        return user

    def partial_update_user(
        self,
        user_id: int,
        update_data: UserPartialUpdate,
    ) -> User | None:
        user = self.get_user_by_id(user_id)
        if user is None:
            return None

        for field, value in update_data.model_dump(exclude_unset=True):
            setattr(user, field, value)

        self.session.commit()
        self.session.refresh(user)
        return user

    def delete_user_by_id(self, user_id: int) -> bool:
        if self.get_user_by_id(user_id) is None:
            return False

        stmt = delete(User).where(User.id == user_id)
        self.session.execute(stmt)
        self.session.commit()
        return True

    def delete_user_by_login(self, login: str) -> bool:
        if self.get_user_by_login(login) is None:
            return False

        stmt = delete(User).where(User.login == login)
        self.session.execute(stmt)
        self.session.commit()
        return True
