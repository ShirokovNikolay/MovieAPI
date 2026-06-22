from core.security.password_utils import hash_password
from schemas.user import UserCreate, UserRegistration


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
