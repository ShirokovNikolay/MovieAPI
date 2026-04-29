import random
import string


def generate_number(start=1, end=1000) -> int:
    return random.randint(start, end)


def generate_numbers(
    list_length: int = 5,
    start: int = 1,
    end: int = 1000,
) -> list[int]:
    return [generate_number(start, end) for _ in range(list_length)]


def generate_string(
    min_string_length: int = 1,
    max_string_length: int = 10,
    length: int | None = None,
) -> str:
    if length is None:
        length = random.randint(min_string_length, max_string_length)

    return "".join(
        [
            random.choice(
                string.ascii_letters + string.digits,
            )
            for _ in range(length)
        ],
    )


def generate_strings(
    min_string_length: int = 1,
    max_string_length: int = 10,
    length: int | None = None,
    min_list_length: int = 1,
    max_list_length: int = 5,
    list_length: int | None = None,
) -> list[str]:
    if list_length is None:
        list_length = random.randint(min_list_length, max_list_length)

    return [
        generate_string(
            min_string_length,
            max_string_length,
            length,
        )
        for _ in range(list_length)
    ]


def check_schema_not_none_fields_is_valid(schema, data: dict) -> None:
    for field in schema.model_dump(exclude_none=True):
        assert getattr(schema, field) == data[field]
