from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from models import User
from schemas.user import UserCreate, UserUpdate, UserPartialUpdate


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_user_role(self, user_id: int) -> str | None:
        stmt = select(User.role).where(User.id == user_id)
        return self.session.execute(stmt).scalars().first()

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def user_id_exists(self, user_id: int) -> bool:
        return self.get_user_by_id(user_id) is not None

    def get_user_by_login(self, login: str) -> User | None:
        stmt = select(User).where(User.login == login)
        return self.session.execute(stmt).scalars().first()

    def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.session.execute(stmt).scalars().first()

    def user_login_exists(self, login: str) -> bool:
        return self.get_user_by_login(login) is not None

    def user_email_exists(self, email: str) -> bool:
        return self.get_user_by_email(email) is not None

    def get_all_users(self) -> list[User]:
        stmt = select(User)
        return list(self.session.execute(stmt).scalars().all())

    def create_user(self, create_user_data: UserCreate) -> User:
        user = User(
            **create_user_data.model_dump(exclude={"password"}),
            encrypted_password=create_user_data.password,
        )
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

        for field, value in update_data.model_dump(exclude={"password"}).items():
            setattr(user, field, value)
        user.encrypted_password = update_data.password
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

        for field, value in update_data.model_dump(
            exclude_unset=True,
            exclude={"password"},
        ).items():
            setattr(user, field, value)
        if update_data.password is not None:
            user.encrypted_password = update_data.password
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
