from fastapi import APIRouter, Request

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
async def check_health() -> dict[str, str]:
    return {"status": "ok"}
