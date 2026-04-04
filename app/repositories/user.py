from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from core.constants import UserRole
from models import User
from schemas.user import (
    UserCreate,
    UserUpdate,
    UserPartialUpdate,
)


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user_role(self, user_id: int) -> str | None:
        stmt = select(User.role).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def user_id_exists(self, user_id: int) -> bool:
        return await self.get_user_by_id(user_id) is not None

    async def get_user_by_login(self, login: str) -> User | None:
        stmt = select(User).where(User.login == login)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def user_login_exists(self, login: str) -> bool:
        return await self.get_user_by_login(login) is not None

    async def user_email_exists(self, email: str) -> bool:
        return await self.get_user_by_email(email) is not None

    async def get_all_users(self) -> list[User]:
        stmt = select(User)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_user(self, create_user_data: UserCreate) -> User:
        user = User(
            **create_user_data.model_dump(exclude={"password"}),
            encrypted_password=create_user_data.password,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def make_admin(self, user_id: int) -> bool:
        user = await self.get_user_by_id(user_id)
        if user is not None:
            user.role = UserRole.admin
            await self.session.commit()
            await self.session.refresh(user)
            return True
        return False

    async def update_user(
        self,
        user_id: int,
        update_data: UserUpdate,
    ) -> User | None:
        user = await self.get_user_by_id(user_id)
        if user is None:
            return None

        for field, value in update_data.model_dump(exclude={"password"}).items():
            setattr(user, field, value)
        user.encrypted_password = update_data.password
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def partial_update_user(
        self,
        user_id: int,
        update_data: UserPartialUpdate,
    ) -> User | None:
        user = await self.get_user_by_id(user_id)
        if user is None:
            return None

        for field, value in update_data.model_dump(
            exclude_unset=True,
            exclude={"password"},
        ).items():
            setattr(user, field, value)
        if update_data.password is not None:
            user.encrypted_password = update_data.password
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user_by_id(self, user_id: int) -> bool:
        if await self.get_user_by_id(user_id) is None:
            return False

        stmt = delete(User).where(User.id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return True

    async def delete_user_by_login(self, login: str) -> bool:
        if await self.get_user_by_login(login) is None:
            return False

        stmt = delete(User).where(User.login == login)
        await self.session.execute(stmt)
        await self.session.commit()
        return True
