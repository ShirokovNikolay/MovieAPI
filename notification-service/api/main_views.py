from fastapi import APIRouter, Request

from service import EmailService

router = APIRouter(
    tags=["Main"],
)


@router.get("/")
def read_root(
    request: Request,
    name: str = "Nikolay",
) -> dict[str, str]:
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "message": f"Hello {name}!",
        "docs": str(docs_url),
    }


@router.get("/health")
def check_health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/send")
async def send_email(
    subject: str,
    body: str,
    to_email: str,
) -> None:
    await EmailService.send_email(
        subject=subject,
        body=body,
        to_email=to_email,
    )


@router.get("/welcome-email")
async def send_welcome_email_message(
    email: str,
    name: str,
) -> None:
    await EmailService.send_welcome_email(
        email=email,
        name=name,
    )
