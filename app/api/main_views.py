from fastapi import APIRouter
from starlette.requests import Request


router = APIRouter(
    tags=["Main"],
)


@router.get("/")
def read_root(
    request: Request,
    name: str = "Nikolay",
):
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "message": f"Hello {name}!",
        "docs_url": str(docs_url),
    }


@router.get("/health")
def check_health():
    return {"status": "ok"}
