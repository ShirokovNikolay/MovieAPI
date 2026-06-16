import random
from typing import cast

from packages.celery.constants import Queue, TaskType
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from core.celery.celery_app import app
from core.config import settings
from core.constants import UserRole
from core.exceptions.auth import InvalidPasswordError
from core.exceptions.confirmation_code import (
    EmailConfirmationCodeNotFoundError,
    InvalidEmailConfirmationCodeError,
)
from core.exceptions.user import (
    UserEmailAlreadyExistsError,
    UserIdNotFoundError,
    UserLoginAlreadyExistsError,
    UserLoginNotFoundError,
)
from core.redis import CacheService
from core.security.password_utils import hash_password, verify_password
from packages.schemas import SendEmail
from repositories import UserRepository
from schemas.auth import UserLogin
from schemas.user import (
    UserCreate,
    UserPartialUpdate,
    UserRegistration,
    UserResponse,
    UserResponseList,
    UserUpdate,
)
from services.http_request import HttpRequestService


class UserService:
    def __init__(
        self,
        session: AsyncSession,
        redis_service: CacheService | None = None,
        http_request_service: HttpRequestService | None = None,
    ) -> None:
        self.session = session
        self.user_repository = UserRepository(session)
        self.http_request_service = http_request_service
        self.cache_service = redis_service

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

    async def get_confirmation_code(self, email: EmailStr) -> str:
        confirmation_code = await self.cache_service.get(f"register:email:{email}")
        if confirmation_code is None:
            raise EmailConfirmationCodeNotFoundError(
                email=email,
            )
        return confirmation_code

    async def verify_confirmation_code(
        self,
        email: EmailStr,
        confirmation_code: str,
    ) -> None:
        sent_confirmation_code = await self.get_confirmation_code(email)
        if confirmation_code != sent_confirmation_code:
            raise InvalidEmailConfirmationCodeError(
                email=email,
                confirmation_code=confirmation_code,
            )

    @staticmethod
    def convert_registration_to_create_schema(
        user_registration_data: UserRegistration,
    ) -> UserCreate:
        user_create_data = user_registration_data.model_dump(
            exclude={"confirmation_code", "password"},
        )
        password = user_registration_data.password
        encrypted_password = hash_password(password)
        user_create_data["encrypted_password"] = encrypted_password
        return UserCreate(**user_create_data)

    async def create_user(
        self,
        registration_user_data: UserRegistration,
    ) -> UserResponse:
        if await self.user_repository.user_login_exists(registration_user_data.login):
            raise UserLoginAlreadyExistsError(registration_user_data.login)

        if await self.user_repository.user_email_exists(registration_user_data.email):
            raise UserEmailAlreadyExistsError(registration_user_data.email)

        await self.verify_confirmation_code(
            registration_user_data.email,
            registration_user_data.confirmation_code,
        )

        create_user_data = self.convert_registration_to_create_schema(
            registration_user_data,
        )
        user = await self.user_repository.create_user(create_user_data)
        app.send_task(
            name=TaskType.send_welcome_email.value,
            args=[
                registration_user_data.email,
                registration_user_data.name,
            ],
            queue=Queue.notification.value,
        )
        return UserResponse.model_validate(user)

    async def create_confirmation_code(self, email: EmailStr) -> str:
        confirmation_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        await self.cache_service.set(
            key=f"register:email:{email}",
            value=confirmation_code,
            ttl=60,
        )
        return confirmation_code

    async def send_confirmation_code(self, email: EmailStr) -> None:
        confirmation_code = await self.create_confirmation_code(email)
        subject = "Confirm your email address"
        body = f"Your confirmation code is {confirmation_code}"
        email_data = SendEmail(
            subject=subject,
            body=body,
            to_email=email,
        )
        await self.http_request_service.post(
            url=settings.notificationservice.send_email_endpoint,
            json=email_data.model_dump(),
        )

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
