from tests.utils.data_generators.base import generate_string


def create_token_info_data():
    data = {
        "access_token": generate_string(),
        "refresh_token": generate_string(),
        "token_type": generate_string(),
    }
    return data
