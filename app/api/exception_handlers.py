from fastapi import FastAPI
from fastapi import Request, status
from fastapi.responses import JSONResponse

from core.exceptions.base import (
    NotFoundError,
    ConflictError,
    ForbiddenError,
    AuthenticationError,
)


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(NotFoundError, not_found_exception_handler)
    app.add_exception_handler(ConflictError, conflict_exception_handler)
    app.add_exception_handler(AuthenticationError, authentication_exception_handler)
    app.add_exception_handler(ForbiddenError, forbidden_exception_handler)


def not_found_exception_handler(
    request: Request,
    exception: NotFoundError,
) -> JSONResponse:
    return JSONResponse(
        content={"message": exception.detail},
        status_code=status.HTTP_404_NOT_FOUND,
    )


def conflict_exception_handler(
    request: Request,
    exception: ConflictError,
) -> JSONResponse:
    return JSONResponse(
        content={"message": exception.detail},
        status_code=status.HTTP_409_CONFLICT,
    )


def authentication_exception_handler(
    request: Request,
    exception: AuthenticationError,
) -> JSONResponse:
    return JSONResponse(
        content={"message": exception.detail},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


def forbidden_exception_handler(
    request: Request,
    exception: ForbiddenError,
) -> JSONResponse:
    return JSONResponse(
        content={"message": exception.detail},
        status_code=status.HTTP_403_FORBIDDEN,
    )
