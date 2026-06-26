from enum import StrEnum


class Queue(StrEnum):
    app = "movie-catalog"
    mediaservice = "media-service"
    notification = "notification-service"


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

    prepare_inactive_users = "movie-catalog.email.prepare_inactive_users"
    prepare_newest_movies = "movie-catalog.email.prepare_newest_movies"
    create_chain_user_reminder = "movie-catalog.email.create_chain_user_reminder"
    send_inactive_user_reminder = "notification-service.email.send-inactive-user-email"
