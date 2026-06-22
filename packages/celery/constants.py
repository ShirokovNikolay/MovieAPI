from enum import StrEnum


class Queue(StrEnum):
    mediaservice = "mediaservice"
    notification = "notification-service"


class TaskType(StrEnum):
    delete_temporary_file = "mediaservice.media.delete_temporary_file"
    send_welcome_email = "notification-service.email.send-welcome-email"
    send_confirm_registration_email = (
        "notification-service.email.send-confirm-registration-email"
    )
    send_confirm_login_email = "notification-service.email.confirm-login-email"
    send_reset_password_email_data = (
        "notification-service.email.send_reset_password_email_data"
    )
