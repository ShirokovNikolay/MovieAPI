from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from core.celery.celery_app import app
from core.constants import UserRole
from core.exceptions.auth import InvalidPasswordError
from core.exceptions.user import (
    UserEmailAlreadyExistsError,
    UserIdNotFoundError,
    UserLoginAlreadyExistsError,
    UserLoginNotFoundError,
)
from core.security.password_utils import hash_password, verify_password
from repositories import UserRepository
from schemas.auth import UserLogin
from schemas.user import (
    UserCreate,
    UserPartialUpdate,
    UserResponse,
    UserResponseList,
    UserUpdate,
)


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repository = UserRepository(session)

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        user = await self.user_repository.get_user_by_id(user_id)
        if user is not None:
            return UserResponse.model_validate(user)

        raise UserIdNotFoundError(user_id)

    async def get_user_by_login(self, login: str) -> UserResponse:
        user = await self.user_repository.get_user_by_login(login)
        if user is not None:
            return UserResponse.model_validate(user)

        raise UserLoginNotFoundError(login)

    async def user_login_exists(self, login: str) -> bool:
        return await self.user_repository.user_login_exists(login)

    async def get_all_users(self, size: int = 10, page: int = 1) -> UserResponseList:
        users = [
            UserResponse.model_validate(user)
            for user in await self.user_repository.get_all_users(size, page)
        ]
        return UserResponseList(
            user_list=users,
            size=size,
            page=page,
        )

    async def create_user(self, create_user_data: UserCreate) -> UserResponse:
        if await self.user_repository.user_login_exists(create_user_data.login):
            raise UserLoginAlreadyExistsError(create_user_data.login)

        if await self.user_repository.user_email_exists(create_user_data.email):
            raise UserEmailAlreadyExistsError(create_user_data.email)

        create_user_data.password = hash_password(create_user_data.password)
        user = await self.user_repository.create_user(create_user_data)
        app.send_task(
            name="notification-service.email.send-welcome-email",
            args=[
                create_user_data.email,
                create_user_data.name,
            ],
            queue="notification",
        )
        return UserResponse.model_validate(user)

    async def make_admin(self, user_id: int) -> None:
        if not await self.user_repository.make_admin(user_id):
            raise UserIdNotFoundError(user_id)

    async def update_user(
        self,
        user_id: int,
        update_data: UserUpdate,
    ) -> UserResponse:
        user = await self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise UserIdNotFoundError(user_id)

        if (
            user.login != update_data.login
            and await self.user_repository.user_login_exists(update_data.login)
        ):
            raise UserLoginAlreadyExistsError(update_data.login)

        if (
            user.email != update_data.email
            and await self.user_repository.user_email_exists(update_data.email)
        ):
            raise UserEmailAlreadyExistsError(update_data.email)

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
            raise UserIdNotFoundError(user_id)

        if (
            "login" in update_data.model_fields_set
            and user.login != update_data.login
            and await self.user_repository.user_login_exists(
                cast(str, update_data.login),
            )
        ):
            raise UserLoginAlreadyExistsError(cast(str, update_data.login))

        if (
            "email" in update_data.model_fields_set
            and user.email != update_data.email
            and await self.user_repository.user_email_exists(
                cast(str, update_data.email),
            )
        ):
            raise UserEmailAlreadyExistsError(cast(str, update_data.email))

        if update_data.password is not None:
            update_data.password = hash_password(update_data.password)
        updated_user = await self.user_repository.partial_update_user(
            user_id,
            update_data,
        )
        return UserResponse.model_validate(updated_user)

    async def delete_user_by_id(self, user_id: int) -> None:
        if not await self.user_repository.delete_user_by_id(user_id):
            raise UserIdNotFoundError(user_id)

    async def delete_user_by_login(self, login: str) -> None:
        if not await self.user_repository.delete_user_by_login(login):
            raise UserLoginNotFoundError(login)

    async def authenticate_user(self, login_data: UserLogin) -> UserResponse:
        user = await self.user_repository.get_user_by_login(login_data.login)
        if user is None:
            raise UserLoginNotFoundError(login_data.login)

        if not verify_password(login_data.password, user.encrypted_password):
            raise InvalidPasswordError

        return UserResponse.model_validate(user)

    async def is_admin(self, user_id: int) -> bool:
        role = await self.user_repository.get_user_role(user_id)
        if role is None:
            raise UserIdNotFoundError(user_id)

        return role == UserRole.admin.value
