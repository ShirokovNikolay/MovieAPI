import random
from datetime import datetime

from core.constants import (
    USER_SURNAME_MIN_LENGTH,
    USER_SURNAME_MAX_LENGTH,
    USER_NAME_MIN_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_LOGIN_MIN_LENGTH,
    USER_LOGIN_MAX_LENGTH,
    USER_EMAIL_MIN_LENGTH,
    USER_EMAIL_MAX_LENGTH,
    USER_PASSWORD_MIN_LENGTH,
    USER_PASSWORD_MAX_LENGTH,
)
from schemas.user import UserResponse
from tests.utils.data_generators.base import generate_string, generate_number


def generate_email_fixed_length(length: int) -> str:
    domain_zone = ["com", "net", "org", "ru", "io"]
    dz = random.choice(domain_zone)
    remain_length = length - len(dz) - 2
    local_part_length = random.randint(1, remain_length - 1)
    domain_part_length = remain_length - local_part_length
    local_part = generate_string(length=local_part_length)
    domain_part = generate_string(length=domain_part_length).lower()
    return f"{local_part}@{domain_part}.{dz}"


def generate_random_email_with_length_range(min_length, max_length) -> str:
    email_length = random.randint(min_length, max_length)
    return generate_email_fixed_length(email_length)


def create_user_data() -> dict[str, str]:
    data = {
        "surname": generate_string(
            min_string_length=USER_SURNAME_MIN_LENGTH,
            max_string_length=USER_SURNAME_MAX_LENGTH,
        ),
        "name": generate_string(
            min_string_length=USER_NAME_MIN_LENGTH,
            max_string_length=USER_NAME_MAX_LENGTH,
        ),
        "login": generate_string(
            min_string_length=USER_LOGIN_MIN_LENGTH,
            max_string_length=USER_LOGIN_MAX_LENGTH,
        ),
        "email": generate_random_email_with_length_range(
            min_length=USER_EMAIL_MIN_LENGTH,
            max_length=USER_EMAIL_MAX_LENGTH,
        ),
        "password": generate_string(
            min_string_length=USER_PASSWORD_MIN_LENGTH,
            max_string_length=USER_PASSWORD_MAX_LENGTH,
        ),
    }
    return data


def create_user_response_data() -> dict[str, str | int | datetime]:
    data = create_user_data()
    data["id"] = generate_number()
    data["registration_date"] = datetime(
        year=generate_number(2020, 2025),
        month=generate_number(1, 12),
        day=generate_number(1, 28),
    )
    return data


def create_user_response_list(list_length: int = 5) -> list[UserResponse]:
    result = []
    for i in range(list_length):
        user_data = create_user_response_data()
        user = UserResponse(**user_data)
        result.append(user)
    return result
