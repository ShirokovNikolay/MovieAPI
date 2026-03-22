import uvicorn
from fastapi import FastAPI, Request
from config import settings

app = FastAPI(
    title="Movie API",
    debug=settings.debug,
)


@app.get("/")
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


@app.get("/health")
def check_health():
    return {"status": "ok"}
