from enum import StrEnum


class Queue(StrEnum):
    app = "movie-catalog"
    media_service = "media-service"
    notification_service = "notification-service"


class TaskType(StrEnum):
    delete_temporary_file = "media-service.media.delete_temporary_file"
    send_welcome_email = "notification-service.email.send-welcome-email"
    send_confirm_registration_email = (
        "notification-service.email.send-confirm-registration-email"
    )
    send_confirm_login_email = "notification-service.email.confirm-login-email"
    send_reset_password_email_data = (
        "notification-service.email.send_reset_password_email_data"  # noqa: S105
    )

    create_chain_to_notify_inactive_users = (
        "movie-catalog.celery.create_chain_to_notify_inactive_users"
    )
    get_data_to_send_inactive_users_email = (
        "movie-catalog.mailing-list.get_data_to_send_inactive_users_email"
    )
    send_inactive_users_email = "notification-service.email.send-inactive-users-email"
