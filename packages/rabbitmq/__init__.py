__all__ = (
    "RabbitMQService",
    "get_rabbitmq_service",
)

from .dependencies import get_rabbitmq_service
from .service import RabbitMQService
