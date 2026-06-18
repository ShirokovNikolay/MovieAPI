from enum import StrEnum


class Queue(StrEnum):
    mediaservice = "mediaservice"
    notification = "notification-service"


class TaskType(StrEnum):
    delete_temporary_file = "mediaservice.media.delete_temporary_file"
    send_welcome_email = "notification-service.email.send-welcome-email"
    send_confirmation_email_code = "notification-service.email.confirm_email"
