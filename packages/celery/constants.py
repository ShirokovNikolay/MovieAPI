from enum import StrEnum


class Queue(StrEnum):
    app = "movie-catalog"
    media_service = "media-service"
    notification_service = "notification-service"


class TaskType(StrEnum):
    delete_temporary_file = "media-service.media.delete_temporary_file"
    send_welcome_email = "notification-service.email.send-welcome-email"
    send_registration_confirmation_code_email = (
        "notification-service.email.send-registration-confirmation-code-email"
    )
    send_auth_confirmation_code_email = (
        "notification-service.email.send_auth_confirmation_code_email"
    )
    send_reset_password_confirmation_code_email = "notification-service.email.send_reset_password_confirmation_code_email"  # noqa: S105
    create_chain_to_notify_inactive_users = (
        "movie-catalog.celery.create_chain_to_notify_inactive_users"
    )
    get_data_to_send_inactive_users_email = (
        "movie-catalog.mailing-list.get_data_to_send_inactive_users_email"
    )
    send_inactive_users_email = "notification-service.email.send-inactive-users-email"
