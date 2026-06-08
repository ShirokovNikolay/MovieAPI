__all__ = (
    "RabbitMQService",
    "get_rabbit_mq_service",
)

from .dependencies import get_rabbit_mq_service
from .service import RabbitMQService
