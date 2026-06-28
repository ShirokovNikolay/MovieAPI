import random
from typing import cast

from packages.celery.constants import Queue, TaskType
from pydantic import EmailStr

from core.celery.celery_app import app
from core.config import settings
from core.constants import (
    ATTEMPT_FIELD,
    BEARER_TOKEN_TYPE,
    EMAIL_FIELD,
    LOGIN_FIELD,
    MAX_CONFIRM_CODE_ATTEMPTS,
    ConfirmationCodeType,
)
from core.exceptions.auth import InvalidPasswordError
from core.exceptions.confirmation_code import (
    EmailConfirmationCodeNotFoundError,
    InvalidEmailConfirmationCodeError,
)
from core.exceptions.user import (
    UserEmailAlreadyExistsError,
    UserLoginAlreadyExistsError,
)
from core.redis import RedisService
from core.schema_utils import convert_registration_to_create_schema
from core.security.jwt.token_factory import (
    create_access_token,
    create_auth_token,
    create_recover_token,
    create_registration_token,
    create_reset_password_token,
    create_two_factor_auth_token,
)
from core.security.jwt.utils import decode_jwt
from core.security.password_utils import verify_password
from schemas.auth import (
    RecoverAccountRequest,
    ResetPasswordRequest,
    SendConfirmationCodeRequest,
    UserLogin,
    VerifyUserEmail,
)
from schemas.token_info import TemporaryTokenInfo, TokenInfo
from schemas.user import UserCreate, UserPartialUpdate, UserRegistration
from services import UserService


class AuthService:
    def __init__(
        self,
        user_service: UserService,
        auth_redis_service: RedisService,
    ) -> None:
        self.user_service = user_service
        self.auth_redis_service = auth_redis_service

    async def register_user(
        self,
        user_registration_data: UserRegistration,
    ) -> TemporaryTokenInfo:
        if await self.user_service.user_login_exists(user_registration_data.login):
            raise UserLoginAlreadyExistsError(user_registration_data.login)

        if await self.user_service.user_email_exists(user_registration_data.email):
            raise UserEmailAlreadyExistsError(user_registration_data.email)
        user_create_data = convert_registration_to_create_schema(
            user_registration_data,
        )
        token = create_registration_token(user_registration_data)
        ttl_seconds = settings.jwt.registration.expire_minutes * 60
        key_list = [ConfirmationCodeType.registration.value, token]
        key = ":".join(key_list)
        await self.auth_redis_service.set(
            key=key,
            value=user_create_data,
            ttl=ttl_seconds,
        )
        send_confirmation_code_request = SendConfirmationCodeRequest(
            token=token,
        )
        await self.send_register_confirmation_code(send_confirmation_code_request)
        return TemporaryTokenInfo(
            token=token,
            token_type=BEARER_TOKEN_TYPE,
        )

    async def send_register_confirmation_code(
        self,
        send_confirmation_code_request: SendConfirmationCodeRequest,
    ) -> None:
        token = send_confirmation_code_request.token
        payload = decode_jwt(
            token=token,
            secret_key=settings.jwt.registration.secret_key,
            algorithm=settings.jwt.registration.algorithm,
        )
        email = payload[EMAIL_FIELD]
        confirmation_code = await self.create_confirmation_code(
            email,
            confirmation_code_type=ConfirmationCodeType.registration,
        )
        app.send_task(
            name=TaskType.send_confirm_registration_email.value,
            args=[
                email,
                confirmation_code,
            ],
            queue=Queue.notification_service.value,
        )

    async def verify_register_user(
        self,
        verify_register_user_data: VerifyUserEmail,
    ) -> TokenInfo:
        token = verify_register_user_data.token
        confirmation_code = verify_register_user_data.confirmation_code
        payload = decode_jwt(
            token,
            secret_key=settings.jwt.registration.secret_key,
            algorithm=settings.jwt.registration.algorithm,
        )
        email = payload[EMAIL_FIELD]
        await self.verify_confirmation_code(
            email,
            confirmation_code,
            confirmation_code_type=ConfirmationCodeType.registration,
        )
        key_list = [ConfirmationCodeType.registration.value, token]
        key = ":".join(key_list)
        user_create_data_json = await self.auth_redis_service.get(
            key=key,
        )
        user_create_data = UserCreate.model_validate_json(user_create_data_json)
        user = await self.user_service.create_user(user_create_data)
        await self.auth_redis_service.delete(key)
        return create_auth_token(user)

    async def verify_login_data(self, login_data: UserLogin) -> None:
        encrypted_password = await self.user_service.get_user_encrypted_password(
            login_data.login,
        )
        if not verify_password(login_data.password, encrypted_password):
            raise InvalidPasswordError

    async def authenticate_user(self, login_data: UserLogin) -> TemporaryTokenInfo:
        await self.verify_login_data(login_data)
        user = await self.user_service.get_user_by_login(login_data.login)
        token = create_two_factor_auth_token(user)
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
            secret_key=settings.jwt.two_factor_auth.secret_key,
            algorithm=settings.jwt.two_factor_auth.algorithm,
        )
        email = payload[EMAIL_FIELD]
        confirmation_code = await self.create_confirmation_code(
            email,
            confirmation_code_type=ConfirmationCodeType.two_factor_auth,
        )
        app.send_task(
            name=TaskType.send_confirm_login_email.value,
            args=[
                email,
                confirmation_code,
            ],
            queue=Queue.notification_service.value,
        )

    async def verify_authenticate_user(
        self,
        verify_authenticate_user_data: VerifyUserEmail,
    ) -> TokenInfo:
        token = verify_authenticate_user_data.token
        confirmation_code = verify_authenticate_user_data.confirmation_code
        payload = decode_jwt(
            token,
            secret_key=settings.jwt.two_factor_auth.secret_key,
            algorithm=settings.jwt.two_factor_auth.algorithm,
        )
        email = payload[EMAIL_FIELD]
        await self.verify_confirmation_code(
            email,
            confirmation_code,
            confirmation_code_type=ConfirmationCodeType.two_factor_auth,
        )
        user = await self.user_service.get_user_by_email(email)
        return create_auth_token(user)

    async def get_confirmation_code(
        self,
        email: EmailStr,
        confirmation_code_type: ConfirmationCodeType,
    ) -> str:
        key_list = [confirmation_code_type, email]
        key = ":".join(key_list)
        confirmation_code = await self.auth_redis_service.get(key)
        if confirmation_code is None:
            raise EmailConfirmationCodeNotFoundError(
                email=email,
            )

        return cast(str, confirmation_code)

    async def verify_confirmation_code(
        self,
        email: EmailStr,
        confirmation_code: str,
        confirmation_code_type: ConfirmationCodeType,
    ) -> None:
        sent_confirmation_code = await self.get_confirmation_code(
            email,
            confirmation_code_type,
        )

        key_list = [confirmation_code_type, email]
        key = ":".join(key_list)
        attempt_counter_key_list = [key, ATTEMPT_FIELD]
        attempt_counter_key = ":".join(attempt_counter_key_list)
        await self.auth_redis_service.incr_by(attempt_counter_key)
        count_confirm_code_attempts = await self.auth_redis_service.get(
            attempt_counter_key,
            is_integer=True,
        )
        if count_confirm_code_attempts == MAX_CONFIRM_CODE_ATTEMPTS:
            await self.auth_redis_service.delete(key)
            await self.auth_redis_service.delete(attempt_counter_key)

        if confirmation_code != sent_confirmation_code:
            raise InvalidEmailConfirmationCodeError(
                email=email,
                confirmation_code=confirmation_code,
            )

    async def create_confirmation_code(
        self,
        email: EmailStr,
        confirmation_code_type: ConfirmationCodeType,
    ) -> str:
        confirmation_code = "".join(
            [str(random.randint(0, 9)) for _ in range(6)],  # noqa: S311
        )
        key_list = [confirmation_code_type.value, email]
        key = ":".join(key_list)
        attempt_counter_key_list = [key, ATTEMPT_FIELD]
        attempt_counter_key = ":".join(attempt_counter_key_list)
        await self.auth_redis_service.set(
            key=key,
            value=confirmation_code,
            ttl=60,
        )
        await self.auth_redis_service.set(
            key=attempt_counter_key,
            value=0,
            ttl=60,
        )
        return confirmation_code

    async def recover_account(
        self,
        recover_account_data: RecoverAccountRequest,
    ) -> TemporaryTokenInfo:
        email = recover_account_data.email
        user = await self.user_service.get_user_by_email(email)
        token = create_recover_token(user)
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
            secret_key=settings.jwt.recover.secret_key,
            algorithm=settings.jwt.recover.algorithm,
        )
        login = payload[LOGIN_FIELD]
        email = payload[EMAIL_FIELD]
        confirmation_code = await self.create_confirmation_code(
            email,
            confirmation_code_type=ConfirmationCodeType.recover_password,
        )
        app.send_task(
            name=TaskType.send_reset_password_email_data.value,
            args=[
                login,
                email,
                confirmation_code,
            ],
            queue=Queue.notification_service.value,
        )

    async def verify_recover_account(
        self,
        verify_recover_account_data: VerifyUserEmail,
    ) -> TemporaryTokenInfo:
        token = verify_recover_account_data.token
        confirmation_code = verify_recover_account_data.confirmation_code
        payload = decode_jwt(
            token,
            secret_key=settings.jwt.recover.secret_key,
            algorithm=settings.jwt.recover.algorithm,
        )
        email = payload[EMAIL_FIELD]
        await self.verify_confirmation_code(
            email,
            confirmation_code,
            confirmation_code_type=ConfirmationCodeType.recover_password,
        )
        user = await self.user_service.get_user_by_email(email)
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
            secret_key=settings.jwt.reset_password.secret_key,
            algorithm=settings.jwt.reset_password.algorithm,
        )
        email = payload[EMAIL_FIELD]
        user = await self.user_service.get_user_by_email(email)
        user_partial_update_data = UserPartialUpdate(
            password=reset_password_data.password,
        )
        await self.user_service.partial_update_user(user.id, user_partial_update_data)

    async def refresh_access_token(self, user_id: int) -> TokenInfo:
        user = await self.user_service.get_user_by_id(user_id)
        access_token = create_access_token(user)
        return TokenInfo(access_token=access_token)
