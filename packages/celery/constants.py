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

    prepare_inactive_users = "notification-service.email.prepare_inactive_users"
    prepare_newest_movies = "notification-service.email.prepare_newest_movies"
    send_spam_email = "notification-service.email.send-spam-email"
