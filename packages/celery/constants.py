from enum import StrEnum


class Queue(StrEnum):
    app = "movie-catalog"
    media_service = "media-service"
    notification_service = "notification-service"


class TaskType(StrEnum):
    delete_temporary_file = "media-service.media.delete-temporary-file"
    send_welcome_email = "notification-service.email.send-welcome-email"
    send_registration_confirmation_code_email = (
        "notification-service.email.send-registration-confirmation-code-email"
    )
    send_auth_confirmation_code_email = (
        "notification-service.email.send-auth-confirmation-code-email"
    )
    send_reset_password_confirmation_code_email = "notification-service.email.send-reset-password-confirmation-code-email"  # noqa: S105 E501
    create_chain_to_notify_inactive_users = (
        "movie-catalog.celery.create-chain-to-notify-inactive-users"
    )
    get_data_to_send_inactive_users_email = (
        "movie-catalog.mailing-list.get-data-to-send-inactive-users-email"
    )
    send_inactive_users_email = "notification-service.email.send-inactive-users-email"

    invalidate_movie_detail_cache_by_genre = (
        "movie-catalog.cache.invalidate-movie-detail-cache-by-genre"
    )
