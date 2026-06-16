from fastapi import APIRouter

from packages.schemas import SendEmail
from service import EmailService

router = APIRouter(
    tags=["Send email"],
)


@router.get("/send-welcome-email")
async def send_welcome_email_message(
    email: str,
    name: str,
) -> None:
    await EmailService.send_welcome_email(
        email=email,
        name=name,
    )


@router.post("/send-email")
async def send_email(
    email_data: SendEmail,
) -> None:
    await EmailService.send_email(
        subject=email_data.subject,
        body=email_data.body,
        to_email=email_data.to_email,
    )
