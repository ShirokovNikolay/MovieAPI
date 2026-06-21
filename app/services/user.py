import random
from typing import cast

from packages.celery.constants import Queue, TaskType
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from core.celery.celery_app import app
from core.config import settings
from core.constants import (
    BEARER_TOKEN_TYPE,
    EMAIL_FIELD,
    UserRole,
)
from core.exceptions.auth import InvalidPasswordError
from core.exceptions.confirmation_code import (
    EmailConfirmationCodeNotFoundError,
    InvalidEmailConfirmationCodeError,
)
from core.exceptions.user import (
    UserEmailAlreadyExistsError,
    UserEmailNotFoundError,
    UserIdNotFoundError,
    UserLoginAlreadyExistsError,
    UserLoginNotFoundError,
)
from core.redis import RedisService
from core.security.jwt_utils.token_factory import (
    create_access_token,
    create_recover_token,
    create_refresh_token,
    create_registration_token,
    create_reset_password_token,
    create_two_factor_token,
)
from core.security.jwt_utils.token_factory_utils import (
    decode_jwt,
)
from core.security.password_utils import hash_password, verify_password
from repositories import UserRepository
from schemas.auth import (
    RecoverAccountRequest,
    ResetPasswordRequest,
    SendConfirmationCodeRequest,
    UserLogin,
    VerifyUserEmail,
)
from schemas.token_info import TemporaryTokenInfo, TokenInfo
from schemas.user import (
    UserCreate,
    UserPartialUpdate,
    UserRegistration,
    UserResponse,
    UserResponseList,
    UserUpdate,
)


class UserService:
    def __init__(
        self,
        session: AsyncSession,
        redis_service: RedisService | None = None,
    ) -> None:
        self.session = session
        self.user_repository = UserRepository(session)
        self.redis_service = redis_service

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

    async def get_user_by_email(self, email: EmailStr) -> UserResponse:
        user = await self.user_repository.get_user_by_email(email)
        if user is None:
            raise UserEmailNotFoundError(email)
        return UserResponse.model_validate(user)

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

    async def register_user(
        self,
        registration_user_data: UserRegistration,
    ) -> TemporaryTokenInfo:
        if await self.user_repository.user_login_exists(registration_user_data.login):
            raise UserLoginAlreadyExistsError(registration_user_data.login)

        if await self.user_repository.user_email_exists(registration_user_data.email):
            raise UserEmailAlreadyExistsError(registration_user_data.email)

        create_user_data = self.convert_registration_to_create_schema(
            registration_user_data,
        )
        temporary_token = create_registration_token(registration_user_data)
        ttl_seconds = (
            settings.confirmation_code_jwt.registration_token_expire_minutes * 60
        )
        await self.redis_service.set(
            key=f"{temporary_token}",
            value=create_user_data.model_dump_json(),
            ttl=ttl_seconds,
        )
        send_confirmation_code_request = SendConfirmationCodeRequest(
            token=temporary_token,
        )
        await self.send_register_confirmation_code(send_confirmation_code_request)
        return TemporaryTokenInfo(
            token=temporary_token,
            token_type=BEARER_TOKEN_TYPE,
        )

    async def create_user(self, user: UserCreate) -> UserResponse:
        if await self.user_repository.user_login_exists(user.login):
            raise UserLoginAlreadyExistsError(user.login)

        if await self.user_repository.user_email_exists(user.email):
            raise UserEmailAlreadyExistsError(user.email)

        user = await self.user_repository.create_user(user)
        app.send_task(
            name=TaskType.send_welcome_email.value,
            args=[
                user.email,
                user.name,
            ],
            queue=Queue.notification.value,
        )
        return UserResponse.model_validate(user)

    async def send_register_confirmation_code(
        self,
        send_confirmation_code_request: SendConfirmationCodeRequest,
    ) -> None:
        token = send_confirmation_code_request.token
        payload = decode_jwt(
            token=token,
            secret_key=settings.confirmation_code_jwt.secret_key,
            algorithm=settings.confirmation_code_jwt.algorithm,
        )
        email = payload[EMAIL_FIELD]
        confirmation_code = await self.create_confirmation_code(email)
        app.send_task(
            name=TaskType.send_confirmation_email_code.value,
            args=[
                email,
                confirmation_code,
            ],
            queue=Queue.notification.value,
        )

    async def verify_register_user(
        self,
        verify_register_user_data: VerifyUserEmail,
    ) -> TokenInfo:
        token = verify_register_user_data.token
        confirmation_code = verify_register_user_data.confirmation_code
        payload = decode_jwt(
            token,
            secret_key=settings.confirmation_code_jwt.secret_key,
            algorithm=settings.confirmation_code_jwt.algorithm,
        )
        email = payload[EMAIL_FIELD]
        await self.verify_confirmation_code(
            email,
            confirmation_code,
        )
        user_data_create_json = await self.redis_service.get(key=f"{token}")
        user_data_create = UserCreate.model_validate_json(user_data_create_json)
        user = await self.create_user(user_data_create)
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=BEARER_TOKEN_TYPE,
        )

    async def authenticate_user(self, login_data: UserLogin) -> TemporaryTokenInfo:
        user = await self.user_repository.get_user_by_login(login_data.login)
        if user is None:
            raise UserLoginNotFoundError(login_data.login)

        if not verify_password(login_data.password, user.encrypted_password):
            raise InvalidPasswordError

        user = UserResponse.model_validate(user)
        token = create_two_factor_token(user)
        send_confirmation_code_request = SendConfirmationCodeRequest(
            token=token,
        )
        await self.send_authenticate_confirmation_code(send_confirmation_code_request)
        return TemporaryTokenInfo(
            token=token,
            token_type=BEARER_TOKEN_TYPE,
        )

    async def send_authenticate_confirmation_code(
        self,
        send_confirmation_code_request: SendConfirmationCodeRequest,
    ) -> None:
        token = send_confirmation_code_request.token
        payload = decode_jwt(
            token=token,
            secret_key=settings.confirmation_code_jwt.secret_key,
            algorithm=settings.confirmation_code_jwt.algorithm,
        )
        email = payload[EMAIL_FIELD]
        confirmation_code = await self.create_confirmation_code(email)
        app.send_task(
            name=TaskType.send_confirmation_email_code.value,
            args=[
                email,
                confirmation_code,
            ],
            queue=Queue.notification.value,
        )

    async def verify_authenticate_user(
        self,
        verify_authenticate_user_data: VerifyUserEmail,
    ) -> TokenInfo:
        token = verify_authenticate_user_data.token
        confirmation_code = verify_authenticate_user_data.confirmation_code
        payload = decode_jwt(
            token,
            secret_key=settings.confirmation_code_jwt.secret_key,
            algorithm=settings.confirmation_code_jwt.algorithm,
        )
        email = payload[EMAIL_FIELD]
        await self.verify_confirmation_code(
            email,
            confirmation_code,
        )
        user = await self.get_user_by_email(email)
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=BEARER_TOKEN_TYPE,
        )

    async def get_confirmation_code(self, email: EmailStr) -> str:
        confirmation_code = await self.redis_service.get(f"auth:email:{email}")
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

    async def create_confirmation_code(self, email: EmailStr) -> str:
        confirmation_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        await self.redis_service.set(
            key=f"auth:email:{email}",
            value=confirmation_code,
            ttl=60,
        )
        return confirmation_code

    async def recover_account(
        self,
        recover_account_data: RecoverAccountRequest,
    ) -> TemporaryTokenInfo:
        email = recover_account_data.email
        token = create_recover_token(email)
        send_confirmation_code_request = SendConfirmationCodeRequest(
            token=token,
        )
        await self.send_recover_account_confirmation_code(
            send_confirmation_code_request,
        )
        return TemporaryTokenInfo(
            token=token,
            token_type=BEARER_TOKEN_TYPE,
        )

    async def send_recover_account_confirmation_code(
        self,
        send_confirmation_code_request: SendConfirmationCodeRequest,
    ) -> None:
        token = send_confirmation_code_request.token
        payload = decode_jwt(
            token,
            secret_key=settings.confirmation_code_jwt.secret_key,
            algorithm=settings.confirmation_code_jwt.algorithm,
        )
        email = payload[EMAIL_FIELD]
        confirmation_code = await self.create_confirmation_code(email)
        app.send_task(
            name=TaskType.send_confirmation_email_code.value,
            args=[
                email,
                confirmation_code,
            ],
            queue=Queue.notification.value,
        )

    async def verify_recover_account(
        self,
        verify_recover_account_data: VerifyUserEmail,
    ) -> TemporaryTokenInfo:
        token = verify_recover_account_data.token
        confirmation_code = verify_recover_account_data.confirmation_code
        payload = decode_jwt(
            token,
            secret_key=settings.confirmation_code_jwt.secret_key,
            algorithm=settings.confirmation_code_jwt.algorithm,
        )
        email = payload[EMAIL_FIELD]
        await self.verify_confirmation_code(email, confirmation_code)
        user = await self.get_user_by_email(email)
        reset_password_token = create_reset_password_token(user)
        return TemporaryTokenInfo(
            token=reset_password_token,
            token_type=BEARER_TOKEN_TYPE,
        )

    async def reset_password(self, reset_password_data: ResetPasswordRequest) -> None:
        token = reset_password_data.reset_password_token
        password = reset_password_data.password
        password_confirmation = reset_password_data.password_confirmation
        if password != password_confirmation:
            raise InvalidPasswordError

        payload = decode_jwt(
            token,
            secret_key=settings.confirmation_code_jwt.secret_key,
            algorithm=settings.confirmation_code_jwt.algorithm,
        )
        email = payload[EMAIL_FIELD]
        user = await self.get_user_by_email(email)
        user_partial_update_data = UserPartialUpdate(
            password=reset_password_data.password,
        )
        await self.partial_update_user(user.id, user_partial_update_data)

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

    async def is_admin(self, user_id: int) -> bool:
        role = await self.user_repository.get_user_role(user_id)
        if role is None:
            raise UserIdNotFoundError(user_id)

        return role == UserRole.admin.value

    async def make_admin(self, user_id: int) -> None:
        if not await self.user_repository.make_admin(user_id):
            raise UserIdNotFoundError(user_id)

    async def refresh_access_token(self, user_id: int) -> TokenInfo:
        user = await self.get_user_by_id(user_id)
        access_token = create_access_token(user)
        return TokenInfo(access_token=access_token)
