from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import UserRole
from core.security.password_utils import hash_password, verify_password
from fastapi import HTTPException, status
from repositories import UserRepository
from schemas.user import (
    UserResponse,
    UserResponseList,
    UserCreate,
    UserUpdate,
    UserPartialUpdate,
    UserLogin,
)


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repository = UserRepository(session)

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        user = await self.user_repository.get_user_by_id(user_id)
        if user is not None:
            return UserResponse.model_validate(user)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {user_id=} not found",
        )

    async def get_user_by_login(self, login: str) -> UserResponse:
        user = await self.user_repository.get_user_by_login(login)
        if user is not None:
            return UserResponse.model_validate(user)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {login=} not found",
        )

    async def get_all_users(self) -> UserResponseList:
        users = [
            UserResponse.model_validate(user)
            for user in await self.user_repository.get_all_users()
        ]
        return UserResponseList(user_list=users)

    async def create_user(self, create_user_data: UserCreate) -> UserResponse:
        if await self.user_repository.user_login_exists(create_user_data.login):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with login={create_user_data.login} already exists",
            )

        if await self.user_repository.user_email_exists(create_user_data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email={create_user_data.email} already exists",
            )

        create_user_data.password = hash_password(create_user_data.password)
        user = await self.user_repository.create_user(create_user_data)
        return UserResponse.model_validate(user)

    async def update_user(
        self,
        user_id: int,
        update_data: UserUpdate,
    ) -> UserResponse:
        user = await self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id={user_id} not found",
            )

        if (
            user.login != update_data.login
            and await self.user_repository.user_login_exists(update_data.login)
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with login={update_data.login} already exists",
            )

        if (
            user.email != update_data.email
            and await self.user_repository.user_email_exists(update_data.email)
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email={update_data.email} already exists",
            )

        update_data.password = hash_password(update_data.password)
        updated_user = await self.user_repository.update_user(user_id, update_data)
        return UserResponse.model_validate(updated_user)

    async def partial_update_user(
        self,
        user_id: int,
        update_data: UserPartialUpdate,
    ) -> UserResponse:
        user = await self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id={user_id} not found",
            )

        if (
            "login" in update_data.model_fields_set
            and user.login != update_data.login
            and await self.user_repository.user_login_exists(update_data.login)
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with login={update_data.login} already exists",
            )

        if (
            "email" in update_data.model_fields_set
            and user.email != update_data.email
            and await self.user_repository.user_email_exists(update_data.email)
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email={update_data.email} already exists",
            )

        if update_data.password is not None:
            update_data.password = hash_password(update_data.password)
        updated_user = await self.user_repository.partial_update_user(
            user_id, update_data
        )
        return UserResponse.model_validate(updated_user)

    async def delete_user_by_id(self, user_id: int) -> None:
        if not await self.user_repository.delete_user_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id={user_id} not found",
            )

    async def delete_user_by_login(self, login: str) -> None:
        if not await self.user_repository.delete_user_by_login(login):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with login={login} not found",
            )

    async def authenticate_user(self, login_data: UserLogin) -> UserResponse:
        user = await self.user_repository.get_user_by_login(login_data.login)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invalid login",
            )

        if not verify_password(login_data.password, user.encrypted_password):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid password",
            )

        return UserResponse.model_validate(user)

    async def is_admin(self, user_id: int) -> bool:
        role = await self.user_repository.get_user_role(user_id)
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id={user_id} not found",
            )

        return role == UserRole.admin.value
