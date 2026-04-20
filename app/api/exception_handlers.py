from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from core.exceptions.base import (
    AuthenticationError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    TooManyRequestsError,
)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(NotFoundError, not_found_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(ConflictError, conflict_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(AuthenticationError, authentication_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(ForbiddenError, forbidden_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(TooManyRequestsError, too_many_requests_exception_handler)  # type: ignore[arg-type]


def not_found_exception_handler(
    request: Request,  # noqa: ARG001
    exception: NotFoundError,
) -> JSONResponse:
    return JSONResponse(
        content={"message": exception.detail},
        status_code=status.HTTP_404_NOT_FOUND,
    )


def conflict_exception_handler(
    request: Request,  # noqa: ARG001
    exception: ConflictError,
) -> JSONResponse:
    return JSONResponse(
        content={"message": exception.detail},
        status_code=status.HTTP_409_CONFLICT,
    )


def authentication_exception_handler(
    request: Request,  # noqa: ARG001
    exception: AuthenticationError,
) -> JSONResponse:
    return JSONResponse(
        content={"message": exception.detail},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


def forbidden_exception_handler(
    request: Request,  # noqa: ARG001
    exception: ForbiddenError,
) -> JSONResponse:
    return JSONResponse(
        content={"message": exception.detail},
        status_code=status.HTTP_403_FORBIDDEN,
    )


def too_many_requests_exception_handler(
    request: Request,  # noqa: ARG001
    exception: TooManyRequestsError,
) -> JSONResponse:
    return JSONResponse(
        content={"message": exception.detail},
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    )
