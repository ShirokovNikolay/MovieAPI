import json
from typing import Any

from aio_pika import IncomingMessage, Message


def get_message(
    message: IncomingMessage,
) -> dict[Any, Any]:
    decoded_body = message.body.decode()
    body_dictionary = json.loads(decoded_body)
    return body_dictionary  # type: ignore[no-any-return]


def create_message(body: dict[Any, Any]) -> Message:
    body_string = json.dumps(body)
    encoded_body = body_string.encode()
    message = Message(body=encoded_body)
    return message
